from abc import ABC, abstractmethod


class IOrdenService(ABC):

    @abstractmethod
    def crear_orden(self, data):
        """Valida el pedido (incluida la validacion inter-servicio del
        cliente) y registra la orden. Devuelve la entidad Orden."""
        raise NotImplementedError

    @abstractmethod
    def listar_ordenes(self, limite, offset):
        """Devuelve (lista_de_ordenes, total)."""
        raise NotImplementedError

    @abstractmethod
    def obtener_orden(self, orden_id):
        """Devuelve una entidad Orden o lanza NoEncontradoError."""
        raise NotImplementedError

    @abstractmethod
    def eliminar_orden(self, orden_id):
        """Elimina una orden por su ID."""
        raise NotImplementedError

    @abstractmethod
    def resumen_orden(self, orden_id):
        """Agrega la orden con los datos completos del cliente (composicion)."""
        raise NotImplementedError
