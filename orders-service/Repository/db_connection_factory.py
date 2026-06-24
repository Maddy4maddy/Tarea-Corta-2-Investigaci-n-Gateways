import logging
from pymongo import MongoClient
from config import Config

logger = logging.getLogger(__name__)


class DbConnectionFactory:

    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            logger.info(f"[Repository] Conectando a MongoDB: {Config.MONGODB_URI}")
            cls._client = MongoClient(Config.MONGODB_URI)
        return cls._client

    @classmethod
    def get_database(cls):
        return cls.get_client()[Config.MONGODB_DB]
