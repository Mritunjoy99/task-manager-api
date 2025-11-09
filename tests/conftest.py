import pytest
from app import create_app
from app.extensions import mongo


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')

    with app.app_context():
        # Clear test database
        mongo.db.users.delete_many({})
        mongo.db.tasks.delete_many({})

    yield app

    with app.app_context():
        # Cleanup after tests
        mongo.db.users.delete_many({})
        mongo.db.tasks.delete_many({})


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()
