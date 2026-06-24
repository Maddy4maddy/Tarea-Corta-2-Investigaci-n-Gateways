import logging
from Repository.db_connection_factory import DbConnectionFactory
from Entities.orden import Orden

logger = logging.getLogger(__name__)


class OrdenRepository:

    COLLECTION = 'ordenes'

    @property
    def collection(self):
        # Se resuelve de forma perezosa para no abrir conexion al importar.
        return DbConnectionFactory.get_database()[self.COLLECTION]

    def crear(self, orden: Orden) -> Orden:
        self.collection.insert_one(orden.to_dict())
        logger.info(f"[Repository] Orden insertada: {orden.id}")
        return orden

    def listar(self, limite: int = 100, offset: int = 0):
        documentos = (
            self.collection.find()
            .sort('fechaCreacion', -1)
            .skip(offset)
            .limit(limite)
        )
        return [Orden.from_dict(d) for d in documentos]

    def contar(self) -> int:
        return self.collection.count_documents({})

    def obtener_por_id(self, orden_id: str):
        documento = self.collection.find_one({'_id': orden_id})
        return Orden.from_dict(documento) if documento else None

    def eliminar(self, orden_id: str) -> bool:
        resultado = self.collection.delete_one({'_id': orden_id})
        if resultado.deleted_count > 0:
            logger.info(f"[Repository] Orden eliminada: {orden_id}")
            return True
        return False
