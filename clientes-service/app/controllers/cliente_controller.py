from flask import request, jsonify
from ..models.cliente import Cliente
from ..config import Config
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

def get_db():
    try:
        client = MongoClient(Config.MONGODB_URI)
        return client[Config.MONGODB_DB]
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {str(e)}")
        raise

def registrar_cliente():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()
        
        campos_requeridos = ['nombre', 'email', 'telefono', 'direccion']
        campos_faltantes = [campo for campo in campos_requeridos if not data.get(campo)]
        
        if campos_faltantes:
            return jsonify({
                'error': 'Campos requeridos faltantes',
                'campos_faltantes': campos_faltantes
            }), 400
        
        db = get_db()
        
        cliente_existente = Cliente.obtener_cliente_por_email(db, data['email'])
        if cliente_existente:
            return jsonify({
                'error': 'El email ya esta registrado',
                'email': data['email']
            }), 400
        
        nuevo_cliente = Cliente.crear_cliente(db, data)
        
        logger.info(f"Cliente registrado: {nuevo_cliente['email']} (ID: {nuevo_cliente['_id']})")
        
        return jsonify({
            'mensaje': 'Cliente registrado exitosamente',
            'cliente': nuevo_cliente
        }), 201
        
    except Exception as e:
        logger.error(f"Error al registrar cliente: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e) if Config.DEBUG else None
        }), 500

def listar_clientes():
    try:
        db = get_db()
        
        limite = request.args.get('limite', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        clientes = Cliente.obtener_todos_clientes(db, limite, offset)
        total = Cliente.contar_clientes(db)
        
        logger.info(f"Listados {len(clientes)} clientes (total: {total})")
        
        return jsonify({
            'total': total,
            'offset': offset,
            'limite': limite,
            'clientes': clientes
        }), 200
        
    except Exception as e:
        logger.error(f"Error al listar clientes: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

def obtener_cliente_por_id(cliente_id):
    try:
        if not cliente_id:
            return jsonify({'error': 'ID de cliente requerido'}), 400
        
        db = get_db()
        cliente = Cliente.obtener_cliente_por_id(db, cliente_id)
        
        if not cliente:
            return jsonify({
                'error': 'Cliente no encontrado',
                'id': cliente_id
            }), 404
        
        logger.info(f"Cliente obtenido: {cliente_id}")
        return jsonify(cliente), 200
        
    except Exception as e:
        logger.error(f"Error al obtener cliente {cliente_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

def actualizar_cliente(cliente_id):
    try:
        if not cliente_id:
            return jsonify({'error': 'ID de cliente requerido'}), 400
        
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()
        
        db = get_db()
        
        cliente_existente = Cliente.obtener_cliente_por_id(db, cliente_id)
        if not cliente_existente:
            return jsonify({
                'error': 'Cliente no encontrado',
                'id': cliente_id
            }), 404
        
        if 'email' in data and data['email']:
            cliente_con_email = Cliente.obtener_cliente_por_email(db, data['email'])
            if cliente_con_email and cliente_con_email['_id'] != cliente_id:
                return jsonify({
                    'error': 'El email ya esta registrado por otro cliente',
                    'email': data['email']
                }), 400
        
        cliente_actualizado = Cliente.actualizar_cliente(db, cliente_id, data)
        
        if not cliente_actualizado:
            return jsonify({
                'error': 'No se pudo actualizar el cliente'
            }), 400
        
        logger.info(f"Cliente actualizado: {cliente_id}")
        
        return jsonify({
            'mensaje': 'Cliente actualizado exitosamente',
            'cliente': cliente_actualizado
        }), 200
        
    except Exception as e:
        logger.error(f"Error al actualizar cliente {cliente_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

def eliminar_cliente(cliente_id):
    try:
        if not cliente_id:
            return jsonify({'error': 'ID de cliente requerido'}), 400
        
        db = get_db()
        
        cliente_existente = Cliente.obtener_cliente_por_id(db, cliente_id)
        if not cliente_existente:
            return jsonify({
                'error': 'Cliente no encontrado',
                'id': cliente_id
            }), 404
        
        eliminado = Cliente.eliminar_cliente(db, cliente_id)
        
        if not eliminado:
            return jsonify({
                'error': 'No se pudo eliminar el cliente'
            }), 400
        
        return jsonify({
            'mensaje': 'Cliente eliminado exitosamente',
            'id': cliente_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error al eliminar cliente {cliente_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500