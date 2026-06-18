from flask import Flask, request, jsonify
from flask_cors import CORS
from .config import Config
from .routes.cliente_routes import cliente_bp
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('clientes_service.log')
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    @app.before_request
    def log_request_info():
        logger.info(f"[Clientes Service] {request.method} {request.path}")
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if request.is_json:
                    logger.info(f"Body: {request.get_json()}")
            except:
                pass
    
    app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'clientes',
            'version': '1.0.0'
        }), 200
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Ruta no encontrada'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error interno: {error}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    return app