import json
from app.models.user import User


def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/auth/register',
                           json={
                               'username': 'testuser',
                               'email': 'test@example.com',
                               'password': 'testpass123'
                           })

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'User created successfully'
    assert 'user_id' in data


def test_register_duplicate_username(client):
    """Test registration with duplicate username"""
    # Create first user
    client.post('/api/auth/register',
                json={
                    'username': 'testuser',
                    'email': 'test1@example.com',
                    'password': 'testpass123'
                })

    # Try to create duplicate
    response = client.post('/api/auth/register',
                           json={
                               'username': 'testuser',
                               'email': 'test2@example.com',
                               'password': 'testpass123'
                           })

    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'already exists' in data['message']


def test_login_success(client):
    """Test successful login"""
    # Register user
    client.post('/api/auth/register',
                json={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'password': 'testpass123'
                })

    # Login
    response = client.post('/api/auth/login',
                           json={
                               'username': 'testuser',
                               'password': 'testpass123'
                           })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['username'] == 'testuser'


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login',
                           json={
                               'username': 'nonexistent',
                               'password': 'wrongpass'
                           })

    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Invalid credentials' in data['message']


def test_missing_fields_register(client):
    """Test registration with missing fields"""
    response = client.post('/api/auth/register',
                           json={'username': 'testuser'})

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Missing required fields' in data['message']
