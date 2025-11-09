from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.config import config
from app.extensions import mongo


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    mongo.init_app(app)
    CORS(app)

    # Configure Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Task Manager API",
            "description": "RESTful API for managing tasks with JWT authentication",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
                "email": "support@taskmanager.com"
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        "basePath": "/api",
        "schemes": ["http", "https"],
        "tags": [
            {
                "name": "Authentication",
                "description": "User registration and login endpoints"
            },
            {
                "name": "Tasks",
                "description": "CRUD operations for tasks"
            }
        ]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api')

    # Create indexes
    with app.app_context():
        mongo.db.users.create_index('username', unique=True)
        mongo.db.users.create_index('email', unique=True)
        mongo.db.tasks.create_index('user_id')
        mongo.db.tasks.create_index('created_at')

    return app
