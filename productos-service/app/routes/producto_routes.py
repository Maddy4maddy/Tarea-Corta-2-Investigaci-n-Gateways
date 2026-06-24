from flask import Blueprint

from ..controllers.producto_controller import (
    registrar_producto,
    listar_productos,
    obtener_producto_por_id,
    actualizar_producto,
    eliminar_producto
)

producto_bp = Blueprint(
    'productos',
    __name__
)

@producto_bp.route('/registrar', methods=['POST'])
def registrar():
    return registrar_producto()

@producto_bp.route('/listar', methods=['GET'])
def listar():
    return listar_productos()

@producto_bp.route('/<string:producto_id>', methods=['GET'])
def obtener(producto_id):
    return obtener_producto_por_id(producto_id)

@producto_bp.route('/<string:producto_id>', methods=['PUT'])
def actualizar(producto_id):
    return actualizar_producto(producto_id)

@producto_bp.route('/<string:producto_id>', methods=['DELETE'])
def eliminar(producto_id):
    return eliminar_producto(producto_id)