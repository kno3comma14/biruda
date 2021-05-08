class Config(object):
    DEBUG = True
    TESTING = False
    DATABASE_NAME = "biruda" ## Change for env vars

class DevelopmentConfig(Config):
    SECRET_KEY = "S0m3S3cr3tK3y" ## TODO Change for env vars

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig,
}


    
