import json


def get_auth_token(client):
    """Helper function to get authentication token"""
    # Register user
    client.post('/api/auth/register',
                json={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'password': 'testpass123'
                })

    # Login and get token
    response = client.post('/api/auth/login',
                           json={
                               'username': 'testuser',
                               'password': 'testpass123'
                           })

    data = json.loads(response.data)
    return data['token']


def test_create_task(client):
    """Test task creation"""
    token = get_auth_token(client)

    response = client.post('/api/tasks',
                           headers={'Authorization': f'Bearer {token}'},
                           json={
                               'title': 'Test Task',
                               'description': 'This is a test task'
                           })

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['task']['title'] == 'Test Task'
    assert data['task']['completed'] == False


def test_get_all_tasks(client):
    """Test getting all tasks"""
    token = get_auth_token(client)

    # Create tasks
    client.post('/api/tasks',
                headers={'Authorization': f'Bearer {token}'},
                json={'title': 'Task 1', 'description': 'Description 1'})

    client.post('/api/tasks',
                headers={'Authorization': f'Bearer {token}'},
                json={'title': 'Task 2', 'description': 'Description 2'})

    # Get all tasks
    response = client.get('/api/tasks',
                          headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['tasks']) == 2
    assert data['total'] == 2


def test_get_task_by_id(client):
    """Test getting a specific task"""
    token = get_auth_token(client)

    # Create task
    create_response = client.post('/api/tasks',
                                  headers={'Authorization': f'Bearer {token}'},
                                  json={'title': 'Test Task', 'description': 'Description'})

    task_id = json.loads(create_response.data)['task']['id']

    # Get task
    response = client.get(f'/api/tasks/{task_id}',
                          headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['task']['id'] == task_id


def test_update_task(client):
    """Test task update"""
    token = get_auth_token(client)

    # Create task
    create_response = client.post('/api/tasks',
                                  headers={'Authorization': f'Bearer {token}'},
                                  json={'title': 'Original Title', 'description': 'Original Description'})

    task_id = json.loads(create_response.data)['task']['id']

    # Update task
    response = client.put(f'/api/tasks/{task_id}',
                          headers={'Authorization': f'Bearer {token}'},
                          json={
                              'title': 'Updated Title',
                              'completed': True
                          })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['task']['title'] == 'Updated Title'
    assert data['task']['completed'] == True


def test_delete_task(client):
    """Test task deletion"""
    token = get_auth_token(client)

    # Create task
    create_response = client.post('/api/tasks',
                                  headers={'Authorization': f'Bearer {token}'},
                                  json={'title': 'Test Task', 'description': 'Description'})

    task_id = json.loads(create_response.data)['task']['id']

    # Delete task
    response = client.delete(f'/api/tasks/{task_id}',
                             headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200

    # Verify deletion
    get_response = client.get(f'/api/tasks/{task_id}',
                              headers={'Authorization': f'Bearer {token}'})

    assert get_response.status_code == 404


def test_unauthorized_access(client):
    """Test accessing protected route without token"""
    response = client.get('/api/tasks')

    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Token is missing' in data['message']


def test_pagination(client):
    """Test task pagination"""
    token = get_auth_token(client)

    # Create 15 tasks
    for i in range(15):
        client.post('/api/tasks',
                    headers={'Authorization': f'Bearer {token}'},
                    json={'title': f'Task {i}', 'description': f'Description {i}'})

    # Get first page
    response = client.get('/api/tasks?page=1&per_page=10',
                          headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['tasks']) == 10
    assert data['total'] == 15
    assert data['total_pages'] == 2


def test_filter_by_completed(client):
    """Test filtering tasks by completion status"""
    token = get_auth_token(client)

    # Create completed and incomplete tasks
    response1 = client.post('/api/tasks',
                            headers={'Authorization': f'Bearer {token}'},
                            json={'title': 'Complete Task', 'description': 'Description'})

    task_id = json.loads(response1.data)['task']['id']

    client.put(f'/api/tasks/{task_id}',
               headers={'Authorization': f'Bearer {token}'},
               json={'completed': True})

    client.post('/api/tasks',
                headers={'Authorization': f'Bearer {token}'},
                json={'title': 'Incomplete Task', 'description': 'Description'})

    # Filter completed tasks
    response = client.get('/api/tasks?completed=true',
                          headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 1
    assert data['tasks'][0]['completed'] == True
