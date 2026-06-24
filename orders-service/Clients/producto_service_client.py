import logging
import requests
from config import Config
from Clients.cliente_service_client import ServicioNoDisponibleError

logger = logging.getLogger(__name__)


def _extraer_precio(producto):
    for campo in ('precio', 'price', 'precioUnitario', 'valor'):
        if campo in producto and producto[campo] is not None:
            try:
                return float(producto[campo])
            except (TypeError, ValueError):
                continue
    return None


def _extraer_nombre(producto):
    for campo in ('nombre', 'name', 'titulo', 'descripcion'):
        if campo in producto and producto[campo]:
            return producto[campo]
    return None


class ProductoServiceClient:

    def __init__(self, base_url=None, timeout=None):
        self.base_url = base_url or Config.PRODUCTOS_SERVICE_URL
        self.timeout = timeout or Config.SERVICE_TIMEOUT

    def obtener_producto(self, producto_id):
        """
        Consulta un producto por su ID al microservicio de Productos.

        Devuelve:
            dict  -> si el producto existe.
            None  -> si el producto NO existe (HTTP 404).
        Lanza:
            ServicioNoDisponibleError -> si Productos no responde.
        """
        url = f"{self.base_url}/api/productos/{producto_id}"
        logger.info(f"[inter-servicio] GET Productos -> {url}")

        try:
            respuesta = requests.get(url, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            logger.error(f"[inter-servicio] Error al contactar Productos: {e}")
            raise ServicioNoDisponibleError('productos', str(e))

        if respuesta.status_code == 200:
            producto = respuesta.json()
            if isinstance(producto, dict) and 'producto' in producto:
                producto = producto['producto']
            logger.info(f"[inter-servicio] Producto {producto_id} validado OK")
            return producto

        if respuesta.status_code == 404:
            logger.warning(f"[inter-servicio] Producto {producto_id} no existe")
            return None

        logger.error(f"[inter-servicio] Productos respondio {respuesta.status_code}")
        raise ServicioNoDisponibleError('productos', f"HTTP {respuesta.status_code}")

    def obtener_precio_y_nombre(self, producto):
        """Devuelve (precio, nombre) de un producto de forma tolerante."""
        return _extraer_precio(producto), _extraer_nombre(producto)
