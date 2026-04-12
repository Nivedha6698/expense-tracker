from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from .config import DevConfig, TestConfig, ProdConfig
import logging

db = SQLAlchemy()
jwt = JWTManager()
load_dotenv()

def create_app(config_name=None):
    load_dotenv()
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv("APP_ENV", "dev")


    # ---------------- LOGGING ---------------- #
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    # ---------------- CONFIG SWITCH ---------------- #
    if config_name == "test":
        app.config.from_object(TestConfig)
    elif config_name == "prod":
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    db.init_app(app)
    jwt.init_app(app)

    '''
    load_dotenv()
    app = Flask(__name__)

    # ---------------- LOGGING SETUP ---------------- #
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    app.logger.info("🚀 Flask app starting...")

    # ---------------- ENV ---------------- #
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    # ---------------- CONFIG ---------------- #
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)
    jwt.init_app(app)
    '''

    # ---------------- JWT ERROR HANDLING ---------------- #
    @jwt.unauthorized_loader
    def unauthorized_callback(err):
        return jsonify({"error": "Missing/Invalid token"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        return jsonify({"error": "Invalid token"}), 401

    # ---------------- ROUTES ---------------- #
    from .routes import main
    app.register_blueprint(main)

    # ---------------- DB CREATE ---------------- #
    '''
        with app.app_context():
        from .models import Expense
        db.create_all()
        app.logger.info("✅ Database tables created")
    '''


    return app