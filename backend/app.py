from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(tasks_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return {
            'message': 'DevTask API',
            'version': '1.0',
            'endpoints': {
                'GET /api/tasks': 'Get all tasks',
                'POST /api/tasks': 'Create task',
                'GET /api/tasks/<id>': 'Get single task',
                'PUT /api/tasks/<id>': 'Update task',
                'DELETE /api/tasks/<id>': 'Delete task',
                'GET /api/tasks/stats': 'Get statistics'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
