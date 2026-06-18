from flask import Blueprint, jsonify, request

from app.controllers.orden_controller import *

orden_bp = Blueprint(
    "ordenes",
    __name__
)


@orden_bp.route("/", methods=["GET"])
def listar():

    return jsonify(
        listar_ordenes()
    )


@orden_bp.route("/<id>", methods=["GET"])
def obtener(id):

    return jsonify(
        obtener_orden(id)
    )


@orden_bp.route("/", methods=["POST"])
def crear():

    data = request.json

    return jsonify(
        crear_orden(data)
    )


@orden_bp.route("/<id>", methods=["DELETE"])
def eliminar(id):

    return jsonify(
        eliminar_orden(id)
    )