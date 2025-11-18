from flask import Blueprint, request, jsonify
from models import db, Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get single task"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create new task"""
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task"""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    
    db.session.commit()
    
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200

@tasks_bp.route('/tasks/stats', methods=['GET'])
def get_stats():
    """Get task statistics"""
    total = Task.query.count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    completed = Task.query.filter_by(status='completed').count()
    
    return jsonify({
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed
    }), 200
