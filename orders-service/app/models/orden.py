class Orden:

    def __init__(
        self,
        cliente_id,
        producto_id,
        cantidad,
        total
    ):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.total = total

    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "total": self.total
        }