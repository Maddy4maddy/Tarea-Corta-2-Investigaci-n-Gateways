from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class Producto:

    COLLECTION = 'productos'

    @staticmethod
    def get_collection(db):
        return db[Producto.COLLECTION]

    @staticmethod
    def crear_producto(db, data):

        producto = {
            '_id': str(uuid.uuid4()),
            'nombre': data.get('nombre', '').strip(),
            'descripcion': data.get('descripcion', '').strip(),
            'precio': float(data.get('precio', 0)),
            'stock': int(data.get('stock', 0)),
            'fechaRegistro': datetime.now().isoformat()
        }

        collection = Producto.get_collection(db)

        result = collection.insert_one(producto)

        logger.info(
            f"Producto creado: {result.inserted_id}"
        )

        return producto

    @staticmethod
    def obtener_producto_por_id(db, producto_id):

        collection = Producto.get_collection(db)

        return collection.find_one({
            '_id': producto_id
        })

    @staticmethod
    def obtener_todos_productos(
        db,
        limite=100,
        offset=0
    ):

        collection = Producto.get_collection(db)

        return list(
            collection.find()
            .sort('fechaRegistro', -1)
            .skip(offset)
            .limit(limite)
        )

    @staticmethod
    def contar_productos(db):

        collection = Producto.get_collection(db)

        return collection.count_documents({})

    @staticmethod
    def actualizar_producto(
        db,
        producto_id,
        data
    ):

        collection = Producto.get_collection(db)

        update_data = {}

        campos = [
            'nombre',
            'descripcion',
            'precio',
            'stock'
        ]

        for campo in campos:

            if campo in data:
                update_data[campo] = data[campo]

        if not update_data:
            return None

        producto_actualizado = collection.find_one_and_update(
            {'_id': producto_id},
            {'$set': update_data},
            return_document=True
        )

        return producto_actualizado

    @staticmethod
    def eliminar_producto(
        db,
        producto_id
    ):

        collection = Producto.get_collection(db)

        result = collection.delete_one({
            '_id': producto_id
        })

        return result.deleted_count > 0