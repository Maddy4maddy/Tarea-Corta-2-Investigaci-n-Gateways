import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ---- Servidor ----
    PORT = int(os.getenv('PORT', 5002))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # ---- Base de datos NoSQL (MongoDB) ----
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'ordenes_db')

    # ---- CORS ----
    CORS_ORIGINS = ['*']

    # ---- Comunicacion inter-servicio ----
    # CLIENTES: microservicio ya existente en el repositorio.
    CLIENTES_SERVICE_URL = os.getenv('CLIENTES_SERVICE_URL', 'http://localhost:3003')
    # PRODUCTOS: microservicio de la Persona 1, AUN NO TERMINADO.
    # El cliente esta listo (Clients/producto_service_client.py); se activa
    # poniendo VALIDAR_PRODUCTO=True cuando el servicio de Productos exista.
    PRODUCTOS_SERVICE_URL = os.getenv('PRODUCTOS_SERVICE_URL', 'http://localhost:3001')

    SERVICE_TIMEOUT = int(os.getenv('SERVICE_TIMEOUT', 5))

    # Validacion del cliente: ACTIVA (Clientes ya existe).
    VALIDAR_CLIENTE = os.getenv('VALIDAR_CLIENTE', 'True').lower() == 'true'
    # Validacion del producto: DESACTIVADA por defecto (en espera de Productos).
    # Mientras este en False, el precio_unitario se toma del cuerpo de la peticion.
    # Cuando Productos este listo, poner VALIDAR_PRODUCTO=True y el precio se
    # tomara automaticamente del microservicio de Productos.
    VALIDAR_PRODUCTO = os.getenv('VALIDAR_PRODUCTO', 'False').lower() == 'true'
