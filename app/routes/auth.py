from flask import Blueprint, request, jsonify
from datetime import datetime
from flasgger import swag_from
import jwt
from app.config import Config
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Register a new user',
    'description': 'Create a new user account with username, email, and password',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['username', 'email', 'password'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'john_doe'
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'example': 'john@example.com'
                    },
                    'password': {
                        'type': 'string',
                        'format': 'password',
                        'example': 'securepass123'
                    },
                    'role': {
                        'type': 'string',
                        'enum': ['user', 'admin'],
                        'default': 'user',
                        'example': 'user'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user_id': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Missing required fields'
        },
        409: {
            'description': 'Username or email already exists'
        }
    }
})
def register():
    """Register a new user"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.find_by_username(data['username']):
        return jsonify({'message': 'Username already exists'}), 409

    if User.find_by_email(data['email']):
        return jsonify({'message': 'Email already exists'}), 409

    try:
        user_id = User.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'user')
        )

        return jsonify({
            'message': 'User created successfully',
            'user_id': str(user_id)
        }), 201

    except Exception as e:
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Login user',
    'description': 'Authenticate user and return JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['username', 'password'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'john_doe'
                    },
                    'password': {
                        'type': 'string',
                        'format': 'password',
                        'example': 'securepass123'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'token': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'string'},
                            'username': {'type': 'string'},
                            'email': {'type': 'string'},
                            'role': {'type': 'string'},
                            'created_at': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Missing credentials'
        },
        401: {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    """Login user and return JWT token"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400

    user = User.find_by_username(data['username'])

    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    if not User.verify_password(user['password'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode(
        {
            'user_id': str(user['_id']),
            'username': user['username'],
            'role': user.get('role', 'user'),
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        },
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': User.to_dict(user)
    }), 200
