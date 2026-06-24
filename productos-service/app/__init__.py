from flask import Flask, request, jsonify
from flask_cors import CORS

from .config import Config
from .routes.producto_routes import producto_bp

import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("productos_service.log")
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
            f"[PRODUCTOS] {request.method} {request.path}"
        )

        if request.method in ["POST", "PUT", "PATCH"]:

            try:

                if request.is_json:

                    logger.info(
                        f"Body: {request.get_json()}"
                    )

            except Exception:
                pass

    @app.after_request
    def log_response_info(response):

        logger.info(
            f"Response Status: {response.status}"
        )

        return response

    app.register_blueprint(
        producto_bp,
        url_prefix="/api/productos"
    )

    @app.route("/health", methods=["GET"])
    def health():

        return jsonify({
            "service": "productos-service",
            "status": "UP"
        })

    return app