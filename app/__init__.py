"""Create application"""

from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from .db_config import create_tables, destroy_tables
from app.api.v1 import VERSION1


def create_app():
    """create app"""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    jwt = JWTManager(app)
    #destroy_tables()
    create_tables()
    app.register_blueprint(VERSION1)
    return app
