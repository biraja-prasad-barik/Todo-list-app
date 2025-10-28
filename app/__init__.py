from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database object globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # <-- correct initialization of the extension
    db.init_app(app)

    from .routes.auth import auth_bp
    from .routes.tasks import tasks_bp  # Isko bhi badal dein
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
