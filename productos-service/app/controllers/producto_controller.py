from flask import request, jsonify
from ..models.producto import Producto
from ..config import Config
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


def get_db():

    client = MongoClient(Config.MONGODB_URI)

    return client[Config.MONGODB_DB]

def obtener_producto_por_id(producto_id):

    try:

        db = get_db()

        producto = Producto.obtener_producto_por_id(
            db,
            producto_id
        )

        if not producto:

            return jsonify({
                'error': 'Producto no encontrado',
                'id': producto_id
            }), 404

        return jsonify(producto), 200

    except Exception as e:

        logger.error(str(e))

        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def actualizar_producto(producto_id):

    try:

        if not request.is_json:

            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400

        data = request.get_json()

        db = get_db()

        producto = Producto.obtener_producto_por_id(
            db,
            producto_id
        )

        if not producto:

            return jsonify({
                'error': 'Producto no encontrado'
            }), 404

        actualizado = Producto.actualizar_producto(
            db,
            producto_id,
            data
        )

        return jsonify({
            'mensaje': 'Producto actualizado exitosamente',
            'producto': actualizado
        }), 200

    except Exception as e:

        logger.error(str(e))

        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def eliminar_producto(producto_id):

    try:

        db = get_db()

        eliminado = Producto.eliminar_producto(
            db,
            producto_id
        )

        if not eliminado:

            return jsonify({
                'error': 'Producto no encontrado'
            }), 404

        return jsonify({
            'mensaje': 'Producto eliminado exitosamente',
            'id': producto_id
        }), 200

    except Exception as e:

        logger.error(str(e))

        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def registrar_producto():

    try:

        if not request.is_json:

            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400

        data = request.get_json()

        campos = [
            'nombre',
            'descripcion',
            'precio',
            'stock'
        ]

        faltantes = [
            campo for campo in campos
            if campo not in data
        ]

        if faltantes:

            return jsonify({
                'error': 'Campos requeridos faltantes',
                'campos_faltantes': faltantes
            }), 400

        db = get_db()

        producto = Producto.crear_producto(
            db,
            data
        )

        return jsonify({
            'mensaje': 'Producto registrado exitosamente',
            'producto': producto
        }), 201

    except Exception as e:

        logger.error(str(e))

        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def listar_productos():

    try:

        db = get_db()

        limite = request.args.get(
            'limite',
            100,
            type=int
        )

        offset = request.args.get(
            'offset',
            0,
            type=int
        )

        productos = Producto.obtener_todos_productos(
            db,
            limite,
            offset
        )

        for producto in productos:
            producto['_id'] = str(producto['_id'])

        total = Producto.contar_productos(db)

        return jsonify({
            'total': total,
            'productos': productos
        }), 200

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            'error': str(e)
        }), 500