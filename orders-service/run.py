import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import Config
from Services.orden_service import (
    OrdenService,
    ValidacionError,
    NoEncontradoError,
)
from Clients.cliente_service_client import ServicioNoDisponibleError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('orders_service.log')
    ]
)
logger = logging.getLogger(__name__)

# Instancia del servicio (la conexion a Mongo se abre de forma perezosa).
servicio = OrdenService()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    @app.before_request
    def log_request_info():
        logger.info(f"[Ordenes Service] {request.method} {request.path}")
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if request.is_json:
                    logger.info(f"Body: {request.get_json()}")
            except Exception:
                pass

    # ---------------------------------------------------------------- health
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'ordenes', 'version': '1.0.0'}), 200

    # ----------------------------------------------------------- crear orden
    @app.route('/api/ordenes/', methods=['POST'])
    def crear():
        try:
            if not request.is_json:
                return jsonify({'error': 'Content-Type debe ser application/json'}), 400
            orden = servicio.crear_orden(request.get_json())
            return jsonify({'mensaje': 'Orden creada exitosamente', 'orden': orden.to_dict()}), 201
        except ValidacionError as e:
            respuesta = {'error': e.mensaje}
            if e.detalles:
                respuesta.update(e.detalles)
            return jsonify(respuesta), 400
        except NoEncontradoError as e:
            return jsonify({'error': e.mensaje, **e.info}), 404
        except ServicioNoDisponibleError as e:
            return jsonify({'error': 'No se pudo validar el cliente', 'servicio': e.servicio, 'detalle': str(e)}), 502
        except Exception as e:
            logger.error(f"Error al crear orden: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500

    # --------------------------------------------------------- listar ordenes
    @app.route('/api/ordenes/', methods=['GET'])
    def listar():
        try:
            limite = request.args.get('limite', 100, type=int)
            offset = request.args.get('offset', 0, type=int)
            ordenes, total = servicio.listar_ordenes(limite, offset)
            return jsonify({
                'total': total, 'offset': offset, 'limite': limite,
                'ordenes': [o.to_dict() for o in ordenes]
            }), 200
        except Exception as e:
            logger.error(f"Error al listar ordenes: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500

    # ------------------------------------------- resumen (agregacion) por id
    @app.route('/api/ordenes/resumen/<string:orden_id>', methods=['GET'])
    def resumen(orden_id):
        try:
            return jsonify(servicio.resumen_orden(orden_id)), 200
        except NoEncontradoError as e:
            return jsonify({'error': e.mensaje, **e.info}), 404
        except Exception as e:
            logger.error(f"Error al componer resumen {orden_id}: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500

    # ----------------------------------------------------- obtener orden por id
    @app.route('/api/ordenes/<string:orden_id>', methods=['GET'])
    def obtener(orden_id):
        try:
            orden = servicio.obtener_orden(orden_id)
            return jsonify(orden.to_dict()), 200
        except NoEncontradoError as e:
            return jsonify({'error': e.mensaje, **e.info}), 404
        except Exception as e:
            logger.error(f"Error al obtener orden {orden_id}: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500

    # --------------------------------------------------------- eliminar orden
    @app.route('/api/ordenes/<string:orden_id>', methods=['DELETE'])
    def eliminar(orden_id):
        try:
            servicio.eliminar_orden(orden_id)
            return jsonify({'mensaje': 'Orden eliminada exitosamente', 'id': orden_id}), 200
        except NoEncontradoError as e:
            return jsonify({'error': e.mensaje, **e.info}), 404
        except Exception as e:
            logger.error(f"Error al eliminar orden {orden_id}: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Ruta no encontrada'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error interno: {error}")
        return jsonify({'error': 'Error interno del servidor'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    logger.info("=" * 50)
    logger.info("Servicio Ordenes iniciando...")
    logger.info(f"Puerto: {Config.PORT}")
    logger.info(f"MongoDB URI: {Config.MONGODB_URI}")
    logger.info(f"Base de datos: {Config.MONGODB_DB}")
    logger.info(f"Clientes service: {Config.CLIENTES_SERVICE_URL} (validar={Config.VALIDAR_CLIENTE})")
    logger.info(f"Productos service: {Config.PRODUCTOS_SERVICE_URL} (validar={Config.VALIDAR_PRODUCTO})")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info("=" * 50)
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
