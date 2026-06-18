from bson import ObjectId
from app.config import ordenes_collection


def listar_ordenes():

    resultado = []

    for orden in ordenes_collection.find():

        orden["_id"] = str(orden["_id"])

        resultado.append(orden)

    return resultado


def obtener_orden(id):

    orden = ordenes_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if orden:
        orden["_id"] = str(orden["_id"])

    return orden


def crear_orden(data):

    resultado = ordenes_collection.insert_one(data)

    return {
        "mensaje": "Orden creada correctamente",
        "id": str(resultado.inserted_id)
    }


def eliminar_orden(id):

    resultado = ordenes_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return {
        "eliminados": resultado.deleted_count
    }