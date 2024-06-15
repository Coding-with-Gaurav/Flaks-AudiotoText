
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
