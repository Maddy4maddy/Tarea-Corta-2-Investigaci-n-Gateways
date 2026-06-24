import logging

from Entities.orden import Orden
from Repository.orden_repository import OrdenRepository
from Clients.cliente_service_client import (
    ClienteServiceClient,
    ServicioNoDisponibleError,
)
from Clients.producto_service_client import ProductoServiceClient
from Services.i_orden_service import IOrdenService
from config import Config

logger = logging.getLogger(__name__)


# ---- Excepciones de dominio (run.py las traduce a codigos HTTP) ----
class ValidacionError(Exception):
    def __init__(self, mensaje, detalles=None):
        self.mensaje = mensaje
        self.detalles = detalles
        super().__init__(mensaje)


class NoEncontradoError(Exception):
    def __init__(self, mensaje, info=None):
        self.mensaje = mensaje
        self.info = info or {}
        super().__init__(mensaje)


class OrdenService(IOrdenService):

    def __init__(self, repository=None, cliente_client=None, producto_client=None):
        self.repository = repository or OrdenRepository()
        self.cliente_client = cliente_client or ClienteServiceClient()
        self.producto_client = producto_client or ProductoServiceClient()

    # ------------------------------------------------------------------ crear
    def crear_orden(self, data):
        if not isinstance(data, dict):
            raise ValidacionError('Cuerpo de la solicitud invalido')

        # 1) Campos requeridos basicos
        requeridos = ['cliente_id', 'producto_id', 'cantidad']
        faltantes = [c for c in requeridos if data.get(c) in (None, '')]
        if faltantes:
            raise ValidacionError('Campos requeridos faltantes', {'campos_faltantes': faltantes})

        try:
            cantidad = int(data['cantidad'])
        except (TypeError, ValueError):
            raise ValidacionError('cantidad debe ser un numero entero')
        if cantidad <= 0:
            raise ValidacionError('cantidad debe ser mayor a 0')

        # 2) COMUNICACION INTER-SERVICIO con CLIENTES (obligatoria)
        cliente_nombre = None
        if Config.VALIDAR_CLIENTE:
            cliente = self.cliente_client.obtener_cliente(data['cliente_id'])
            if cliente is None:
                raise NoEncontradoError('El cliente no existe', {'cliente_id': data['cliente_id']})
            cliente_nombre = cliente.get('nombre')

        # 3) PRODUCTO: si el microservicio de Productos ya existe
        #    (VALIDAR_PRODUCTO=True) se valida y se toma su precio real.
        #    Mientras este en espera, el precio se toma del cuerpo.
        producto_nombre = data.get('producto_nombre')
        if Config.VALIDAR_PRODUCTO:
            producto = self.producto_client.obtener_producto(data['producto_id'])
            if producto is None:
                raise NoEncontradoError('El producto no existe', {'producto_id': data['producto_id']})
            precio_unitario, nombre_prod = self.producto_client.obtener_precio_y_nombre(producto)
            if precio_unitario is None:
                raise ValidacionError('El producto no tiene un precio valido')
            if nombre_prod:
                producto_nombre = nombre_prod
        else:
            # Productos aun no esta listo: el precio_unitario es obligatorio en el body.
            if data.get('precio_unitario') in (None, ''):
                raise ValidacionError(
                    'precio_unitario es requerido mientras el servicio de Productos no este activo',
                    {'nota': 'Active VALIDAR_PRODUCTO cuando Productos exista para tomar el precio automaticamente'}
                )
            try:
                precio_unitario = float(data['precio_unitario'])
            except (TypeError, ValueError):
                raise ValidacionError('precio_unitario debe ser numerico')
            if precio_unitario < 0:
                raise ValidacionError('precio_unitario no puede ser negativo')

        # 4) Construir la entidad (calcula total) y persistir
        orden = Orden(
            cliente_id=str(data['cliente_id']).strip(),
            producto_id=str(data['producto_id']).strip(),
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            cliente_nombre=cliente_nombre,
            producto_nombre=producto_nombre
        )
        self.repository.crear(orden)
        logger.info(f"[Service] Orden creada: {orden.id} (total={orden.total})")
        return orden

    # ----------------------------------------------------------------- listar
    def listar_ordenes(self, limite=100, offset=0):
        ordenes = self.repository.listar(limite, offset)
        total = self.repository.contar()
        logger.info(f"[Service] Listadas {len(ordenes)} ordenes (total={total})")
        return ordenes, total

    # ---------------------------------------------------------------- obtener
    def obtener_orden(self, orden_id):
        orden = self.repository.obtener_por_id(orden_id)
        if not orden:
            raise NoEncontradoError('Orden no encontrada', {'id': orden_id})
        return orden

    # --------------------------------------------------------------- eliminar
    def eliminar_orden(self, orden_id):
        orden = self.repository.obtener_por_id(orden_id)
        if not orden:
            raise NoEncontradoError('Orden no encontrada', {'id': orden_id})
        self.repository.eliminar(orden_id)
        logger.info(f"[Service] Orden eliminada: {orden_id}")

    # ---------------------------------------------------------------- resumen
    def resumen_orden(self, orden_id):
        """Agregacion / API Composition: orden + cliente (y producto si esta activo)."""
        orden = self.repository.obtener_por_id(orden_id)
        if not orden:
            raise NoEncontradoError('Orden no encontrada', {'id': orden_id})

        advertencias = []

        cliente = None
        try:
            cliente = self.cliente_client.obtener_cliente(orden.cliente_id)
            if cliente is None:
                advertencias.append('El cliente asociado ya no existe')
        except ServicioNoDisponibleError as e:
            advertencias.append(f"Servicio de clientes no disponible: {e}")

        producto = None
        if Config.VALIDAR_PRODUCTO:
            try:
                producto = self.producto_client.obtener_producto(orden.producto_id)
                if producto is None:
                    advertencias.append('El producto asociado ya no existe')
            except ServicioNoDisponibleError as e:
                advertencias.append(f"Servicio de productos no disponible: {e}")

        resumen = {'orden': orden.to_dict(), 'cliente': cliente, 'producto': producto}
        if advertencias:
            resumen['advertencias'] = advertencias
        logger.info(f"[Service] Resumen compuesto para orden {orden_id}")
        return resumen
