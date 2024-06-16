class Config:
    SECRET_KEY ="AudiotoText"
    MONGO_URI = "mongodb+srv://Codewithgaurav:mcadsvv2023@cluster0.ubkrusi.mongodb.net/user-data"

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
