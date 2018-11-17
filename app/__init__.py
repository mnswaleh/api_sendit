"""Create application"""

from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .db_config import create_tables, destroy_tables
from app.api.v1 import VERSION1


def create_app(obj_config):
    """create app"""
    app = Flask(__name__)
    app.config.from_object(obj_config)
    jwt = JWTManager(app)
    flask_bcrypt = Bcrypt(app)
    with app.app_context():
        #destroy_tables()
        create_tables()
    app.register_blueprint(VERSION1)
    return app
