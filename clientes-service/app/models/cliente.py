from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class Cliente:
    COLLECTION = 'clientes'
    
    @staticmethod
    def get_collection(db):
        return db[Cliente.COLLECTION]
    
    @staticmethod
    def crear_cliente(db, data):
        cliente = {
            '_id': str(uuid.uuid4()),
            'nombre': data.get('nombre', '').strip(),
            'email': data.get('email', '').lower().strip(),
            'telefono': data.get('telefono', '').strip(),
            'direccion': data.get('direccion', '').strip(),
            'fechaRegistro': datetime.now().isoformat()
        }
        
        collection = Cliente.get_collection(db)
        result = collection.insert_one(cliente)
        logger.info(f"Cliente creado con ID: {result.inserted_id}")
        
        return cliente
    
    @staticmethod
    def obtener_cliente_por_email(db, email):
        collection = Cliente.get_collection(db)
        return collection.find_one({'email': email.lower().strip()})
    
    @staticmethod
    def obtener_cliente_por_id(db, cliente_id):
        collection = Cliente.get_collection(db)
        return collection.find_one({'_id': cliente_id})
    
    @staticmethod
    def obtener_todos_clientes(db, limite=100, offset=0):
        collection = Cliente.get_collection(db)
        return list(
            collection.find()
            .sort('fechaRegistro', -1)
            .skip(offset)
            .limit(limite)
        )
    
    @staticmethod
    def contar_clientes(db):
        collection = Cliente.get_collection(db)
        return collection.count_documents({})
    
    @staticmethod
    def actualizar_cliente(db, cliente_id, data):
        collection = Cliente.get_collection(db)
        
        update_data = {}
        campos_permitidos = ['nombre', 'email', 'telefono', 'direccion']
        
        for campo in campos_permitidos:
            if campo in data and data[campo]:
                if campo == 'email':
                    update_data[campo] = data[campo].lower().strip()
                else:
                    update_data[campo] = data[campo].strip()
        
        if not update_data:
            return None
        
        result = collection.find_one_and_update(
            {'_id': cliente_id},
            {'$set': update_data},
            return_document=True
        )
        
        logger.info(f"Cliente actualizado: {cliente_id}")
        return result
    
    @staticmethod
    def eliminar_cliente(db, cliente_id):
        collection = Cliente.get_collection(db)
        result = collection.delete_one({'_id': cliente_id})
        
        if result.deleted_count > 0:
            logger.info(f"Cliente eliminado: {cliente_id}")
            return True
        return False