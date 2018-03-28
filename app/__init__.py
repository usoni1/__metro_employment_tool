from flask import Flask
from config import config
import psycopg2

db_connection = None
def create_app(config_name):
    global db_mongo
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config[config_name].init_app(app)

    hostname = app.config['HOSTNAME']
    username = app.config['USERNAME']
    password = app.config['PASSWORD']
    database = app.config['DATABASE']
    port = app.config['PORT']

    db_connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app