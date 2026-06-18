from flask import Flask, request, jsonify
from flask_cors import CORS
from .config import Config
from .routes.orden_routes import orden_bp
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('orders_service.log')
    ]
)

logger = logging.getLogger(__name__)

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    @app.before_request
    def log_request_info():

        logger.info(
            f"[Orders Service] {request.method} {request.path}"
        )

        if request.method in ['POST', 'PUT', 'PATCH']:

            try:

                if request.is_json:

                    logger.info(
                        f"Body: {request.get_json()}"
                    )

            except:
                pass

    app.register_blueprint(
        orden_bp,
        url_prefix='/api/ordenes'
    )

    @app.route('/health', methods=['GET'])
    def health_check():

        return jsonify({
            'status': 'healthy',
            'service': 'ordenes',
            'version': '1.0.0'
        }), 200

    return app