import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    HOSTNAME = 'localhost'
    USERNAME = 'metro_insight_admin'
    PASSWORD = 'password'
    DATABASE = '_metro_employment_tool'
    PORT = 5433

class ProductionConfig(Config):
    hostname = 'localhost'
    username = 'metro_insight_admin'
    password = 'password'
    database = '_metro_employment_tool'
    port = 5433

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}