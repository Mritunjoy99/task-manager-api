from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models.task import Task
from app.utils.decorators import token_required, admin_required

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Get all tasks',
    'description': 'Retrieve all tasks for the authenticated user with pagination and filtering',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'description': 'Page number'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Number of tasks per page'
        },
        {
            'name': 'completed',
            'in': 'query',
            'type': 'boolean',
            'description': 'Filter by completion status'
        }
    ],
    'responses': {
        200: {
            'description': 'Tasks retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'tasks': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'title': {'type': 'string'},
                                'description': {'type': 'string'},
                                'completed': {'type': 'boolean'},
                                'created_at': {'type': 'string'},
                                'updated_at': {'type': 'string'}
                            }
                        }
                    },
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'},
                    'total_pages': {'type': 'integer'}
                }
            }
        },
        401: {
            'description': 'Unauthorized - Token missing or invalid'
        }
    }
})
def get_tasks(current_user):
    """Get all tasks for the authenticated user with pagination and filtering"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'

    tasks, total = Task.find_all(
        user_id=str(current_user['_id']),
        page=page,
        per_page=per_page,
        completed=completed
    )

    tasks_list = [Task.to_dict(task) for task in tasks]

    return jsonify({
        'tasks': tasks_list,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }), 200


@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Get task by ID',
    'description': 'Retrieve a specific task by its ID',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Task ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Task retrieved successfully'
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Task not found'
        }
    }
})
def get_task(current_user, task_id):
    """Get a specific task by ID"""
    try:
        task = Task.find_by_id(task_id, str(current_user['_id']))

        if not task:
            return jsonify({'message': 'Task not found'}), 404

        return jsonify({'task': Task.to_dict(task)}), 200

    except Exception as e:
        return jsonify({'message': f'Invalid task ID: {str(e)}'}), 400


@tasks_bp.route('/tasks', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Create a new task',
    'description': 'Create a new task for the authenticated user',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['title'],
                'properties': {
                    'title': {
                        'type': 'string',
                        'example': 'Complete project documentation'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Write comprehensive API documentation'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Task created successfully'
        },
        400: {
            'description': 'Title is required'
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
def create_task(current_user):
    """Create a new task"""
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400

    try:
        task_id = Task.create_task(
            user_id=str(current_user['_id']),
            title=data['title'],
            description=data.get('description', '')
        )

        task = Task.find_by_id(str(task_id), str(current_user['_id']))

        return jsonify({
            'message': 'Task created successfully',
            'task': Task.to_dict(task)
        }), 201

    except Exception as e:
        return jsonify({'message': f'Error creating task: {str(e)}'}), 500


@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Update a task',
    'description': 'Update an existing task',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Task ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'},
                    'completed': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Task updated successfully'
        },
        400: {
            'description': 'No valid fields to update'
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Task not found'
        }
    }
})
def update_task(current_user, task_id):
    """Update a task"""
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'completed' in data:
        update_data['completed'] = data['completed']

    if not update_data:
        return jsonify({'message': 'No valid fields to update'}), 400

    try:
        success = Task.update_task(task_id, str(current_user['_id']), update_data)

        if not success:
            return jsonify({'message': 'Task not found'}), 404

        task = Task.find_by_id(task_id, str(current_user['_id']))

        return jsonify({
            'message': 'Task updated successfully',
            'task': Task.to_dict(task)
        }), 200

    except Exception as e:
        return jsonify({'message': f'Error updating task: {str(e)}'}), 400


@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Delete a task',
    'description': 'Delete an existing task',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Task ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Task deleted successfully'
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Task not found'
        }
    }
})
def delete_task(current_user, task_id):
    """Delete a task"""
    try:
        success = Task.delete_task(task_id, str(current_user['_id']))

        if not success:
            return jsonify({'message': 'Task not found'}), 404

        return jsonify({'message': 'Task deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Error deleting task: {str(e)}'}), 400
