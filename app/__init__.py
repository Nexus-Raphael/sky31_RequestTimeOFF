from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
db = SQLAlchemy()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sky31Employees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .admin import admin_bp
    from .user import user_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')

    #    在应用上下文环境中创建数据库表
    with app.app_context():
        db.create_all()

    return app