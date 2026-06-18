from flask import Blueprint
from ..controllers.cliente_controller import (
    registrar_cliente,
    listar_clientes,
    obtener_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente
)

cliente_bp = Blueprint('clientes', __name__)

@cliente_bp.route('/registrar', methods=['POST'])
def registrar():
    return registrar_cliente()

@cliente_bp.route('/listar', methods=['GET'])
def listar():
    return listar_clientes()

@cliente_bp.route('/<string:cliente_id>', methods=['GET'])
def obtener_cliente(cliente_id):
    return obtener_cliente_por_id(cliente_id)

@cliente_bp.route('/<string:cliente_id>', methods=['PUT'])
def actualizar(cliente_id):
    return actualizar_cliente(cliente_id)

@cliente_bp.route('/<string:cliente_id>', methods=['DELETE'])
def eliminar(cliente_id):
    return eliminar_cliente(cliente_id)