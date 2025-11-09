from datetime import datetime
from bson import ObjectId
from app.extensions import mongo


class Task:
    """Task model for MongoDB"""

    @staticmethod
    def create_task(user_id, title, description):
        """Create a new task"""
        task_data = {
            'user_id': user_id,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = mongo.db.tasks.insert_one(task_data)
        return result.inserted_id

    @staticmethod
    def find_all(user_id, page=1, per_page=10, completed=None):
        """Find all tasks for a user with pagination and filtering"""
        query = {'user_id': user_id}

        if completed is not None:
            query['completed'] = completed

        skip = (page - 1) * per_page

        tasks = mongo.db.tasks.find(query).sort(
            'created_at', -1
        ).skip(skip).limit(per_page)

        total = mongo.db.tasks.count_documents(query)

        return list(tasks), total

    @staticmethod
    def find_by_id(task_id, user_id):
        """Find task by ID and user ID"""
        return mongo.db.tasks.find_one({
            '_id': ObjectId(task_id),
            'user_id': user_id
        })

    @staticmethod
    def update_task(task_id, user_id, update_data):
        """Update a task"""
        update_data['updated_at'] = datetime.utcnow()

        result = mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id), 'user_id': user_id},
            {'$set': update_data}
        )

        return result.modified_count > 0

    @staticmethod
    def delete_task(task_id, user_id):
        """Delete a task"""
        result = mongo.db.tasks.delete_one({
            '_id': ObjectId(task_id),
            'user_id': user_id
        })

        return result.deleted_count > 0

    @staticmethod
    def to_dict(task):
        """Convert task document to dictionary"""
        if task:
            return {
                'id': str(task['_id']),
                'title': task['title'],
                'description': task['description'],
                'completed': task['completed'],
                'created_at': task['created_at'].isoformat(),
                'updated_at': task['updated_at'].isoformat()
            }
        return None
