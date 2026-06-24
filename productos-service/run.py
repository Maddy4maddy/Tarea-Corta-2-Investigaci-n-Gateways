from app import create_app
from app.config import Config
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    app = create_app()

    logger.info("=" * 50)
    logger.info("Servicio Productos iniciando...")
    logger.info(f"Puerto: {Config.PORT}")
    logger.info(f"MongoDB URI: {Config.MONGODB_URI}")
    logger.info(f"Base de datos: {Config.MONGODB_DB}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info("=" * 50)

    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )