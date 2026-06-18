import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.getenv('PORT', 3003))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'clientes_db')
    CORS_ORIGINS = ['*']
    
    @staticmethod
    def get_db_uri():
        return Config.MONGODB_URI