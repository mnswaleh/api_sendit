"""Create application"""

from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.api.v1 import VERSION1
from app.api.v2 import VERSION2
from .db_config import create_tables, destroy_tables

blacklist = set()

def create_app(obj_config):
    """create app"""
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(obj_config)
    jwt = JWTManager(app)
    flask_bcrypt = Bcrypt(app)
    with app.app_context():
        if obj_config == "app.config.TestingConfig":
            destroy_tables()
        create_tables()
    app.register_blueprint(VERSION1)
    app.register_blueprint(VERSION2)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    return app
