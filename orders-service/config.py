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

    # ---- Comunicacion inter-servicio (OBLIGATORIA) ----
    # Para crear una orden, este microservicio consulta a Clientes y a Productos
    # y valida que ambos existan antes de registrar el pedido.
    CLIENTES_SERVICE_URL = os.getenv('CLIENTES_SERVICE_URL', 'http://localhost:3003')
    PRODUCTOS_SERVICE_URL = os.getenv('PRODUCTOS_SERVICE_URL', 'http://localhost:3001')

    SERVICE_TIMEOUT = int(os.getenv('SERVICE_TIMEOUT', 5))

    # Validacion contra Clientes: ACTIVA. Verifica que el cliente exista.
    VALIDAR_CLIENTE = os.getenv('VALIDAR_CLIENTE', 'True').lower() == 'true'
    # Validacion contra Productos: ACTIVA. Verifica que el producto exista y
    # toma su precio real (el precio NO se confia al cuerpo de la peticion).
    VALIDAR_PRODUCTO = os.getenv('VALIDAR_PRODUCTO', 'True').lower() == 'true'
