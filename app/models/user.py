from datetime import datetime
import bcrypt
from bson import ObjectId
from app.extensions import mongo


class User:
    """User model for MongoDB"""

    @staticmethod
    def create_user(username, email, password, role='user'):
        """Create a new user with hashed password"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = mongo.db.users.insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        return mongo.db.users.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify password"""
        return bcrypt.checkpw(
            provided_password.encode('utf-8'),
            stored_password
        )

    @staticmethod
    def to_dict(user):
        """Convert user document to dictionary"""
        if user:
            return {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'role': user.get('role', 'user'),
                'created_at': user['created_at'].isoformat()
            }
        return None
