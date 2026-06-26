from flask import request, jsonify
from ..models.producto import Producto
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


def validar_producto(data, actualizacion=False):

    campos_requeridos = [
        'nombre',
        'descripcion',
        'precio',
        'stock'
    ]

    if not actualizacion:

        campos_faltantes = []

        for campo in campos_requeridos:

            if campo not in data:
                campos_faltantes.append(campo)

            elif data[campo] is None:
                campos_faltantes.append(campo)

            elif isinstance(data[campo], str) and not data[campo].strip():
                campos_faltantes.append(campo)

        if campos_faltantes:
            return {
                'error': 'Campos requeridos faltantes',
                'campos_faltantes': campos_faltantes
            }

    if 'nombre' in data:

        if not str(data['nombre']).strip():
            return {
                'error': 'El nombre es requerido'
            }

    if 'descripcion' in data:

        if not str(data['descripcion']).strip():
            return {
                'error': 'La descripción es requerida'
            }

    if 'precio' in data:

        try:

            precio = float(data['precio'])

            if precio <= 0:
                return {
                    'error': 'El precio debe ser mayor que cero'
                }

        except (ValueError, TypeError):

            return {
                'error': 'Precio inválido'
            }

    if 'stock' in data:

        try:

            stock = int(data['stock'])

            if stock < 0:
                return {
                    'error': 'El stock no puede ser negativo'
                }

        except (ValueError, TypeError):

            return {
                'error': 'Stock inválido'
            }

    return None


def registrar_producto():

    try:

        if not request.is_json:

            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400

        data = request.get_json()

        validacion = validar_producto(data)

        if validacion:
            return jsonify(validacion), 400

        db = get_db()

        producto = Producto.crear_producto(
            db,
            data
        )

        logger.info(
            f"Producto registrado: {producto['nombre']} (ID: {producto['_id']})"
        )

        return jsonify({
            'mensaje': 'Producto registrado exitosamente',
            'producto': producto
        }), 201

    except Exception as e:

        logger.error(f"Error al registrar producto: {str(e)}")

        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e) if Config.DEBUG else None
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

        logger.info(
            f"Listados {len(productos)} productos (total: {total})"
        )

        return jsonify({
            'total': total,
            'offset': offset,
            'limite': limite,
            'productos': productos
        }), 200

    except Exception as e:

        logger.error(
            f"Error al listar productos: {str(e)}"
        )

        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e) if Config.DEBUG else None
        }), 500


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

        producto['_id'] = str(producto['_id'])

        return jsonify(producto), 200

    except Exception as e:

        logger.error(
            f"Error al obtener producto {producto_id}: {str(e)}"
        )

        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e) if Config.DEBUG else None
        }), 500


def actualizar_producto(producto_id):

    try:

        if not request.is_json:

            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400

        data = request.get_json()

        validacion = validar_producto(
            data,
            actualizacion=True
        )

        if validacion:
            return jsonify(validacion), 400

        db = get_db()

        producto_existente = Producto.obtener_producto_por_id(
            db,
            producto_id
        )

        if not producto_existente:

            return jsonify({
                'error': 'Producto no encontrado',
                'id': producto_id
            }), 404

        producto_actualizado = Producto.actualizar_producto(
            db,
            producto_id,
            data
        )

        if not producto_actualizado:

            return jsonify({
                'error': 'No se pudo actualizar el producto'
            }), 400

        producto_actualizado['_id'] = str(
            producto_actualizado['_id']
        )

        return jsonify({
            'mensaje': 'Producto actualizado exitosamente',
            'producto': producto_actualizado
        }), 200

    except Exception as e:

        logger.error(
            f"Error al actualizar producto {producto_id}: {str(e)}"
        )

        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e) if Config.DEBUG else None
        }), 500


def eliminar_producto(producto_id):

    try:

        db = get_db()

        producto_existente = Producto.obtener_producto_por_id(
            db,
            producto_id
        )

        if not producto_existente:

            return jsonify({
                'error': 'Producto no encontrado',
                'id': producto_id
            }), 404

        eliminado = Producto.eliminar_producto(
            db,
            producto_id
        )

        if not eliminado:

            return jsonify({
                'error': 'No se pudo eliminar el producto'
            }), 400

        return jsonify({
            'mensaje': 'Producto eliminado exitosamente',
            'id': producto_id
        }), 200

    except Exception as e:

        logger.error(
            f"Error al eliminar producto {producto_id}: {str(e)}"
        )

        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e) if Config.DEBUG else None
        }), 500