from datetime import datetime
import uuid


class Orden:

    def __init__(
        self,
        cliente_id,
        producto_id,
        cantidad,
        precio_unitario=None,
        cliente_nombre=None,
        producto_nombre=None,
        total=None,
        estado='creada',
        _id=None,
        fecha_creacion=None
    ):
        self.id = _id or str(uuid.uuid4())
        self.cliente_id = cliente_id
        self.cliente_nombre = cliente_nombre
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

        # El total se calcula en el servidor a partir del precio y la cantidad.
        if total is not None:
            self.total = total
        elif precio_unitario is not None and cantidad is not None:
            self.total = round(float(precio_unitario) * int(cantidad), 2)
        else:
            self.total = None

        self.estado = estado
        self.fecha_creacion = fecha_creacion or datetime.now().isoformat()

    def to_dict(self):
        """Convierte la entidad al documento que se almacena en MongoDB."""
        return {
            '_id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente_nombre,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto_nombre,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'total': self.total,
            'estado': self.estado,
            'fechaCreacion': self.fecha_creacion
        }

    @staticmethod
    def from_dict(documento):
        """Reconstruye una entidad Orden desde un documento de MongoDB."""
        return Orden(
            _id=documento.get('_id'),
            cliente_id=documento.get('cliente_id'),
            cliente_nombre=documento.get('cliente_nombre'),
            producto_id=documento.get('producto_id'),
            producto_nombre=documento.get('producto_nombre'),
            cantidad=documento.get('cantidad'),
            precio_unitario=documento.get('precio_unitario'),
            total=documento.get('total'),
            estado=documento.get('estado', 'creada'),
            fecha_creacion=documento.get('fechaCreacion')
        )
