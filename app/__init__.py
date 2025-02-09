from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

# 初始化 SQLAlchemy 对象，但不传入 app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sky31Employees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    # 导入蓝图
    from app.admin import admin_bp
    from app.user import user_bp

    # 注册管理员蓝图
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 注册用户蓝图
    app.register_blueprint(user_bp, url_prefix='/user')

    return app