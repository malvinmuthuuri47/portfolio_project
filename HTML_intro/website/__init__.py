from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Thisisthekey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')


    from .models import User, Hotels

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.context_processor
    def global_var():
        user=current_user
        return {'user': user}

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')