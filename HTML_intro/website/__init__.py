from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')   # Create an absolute path for the database file
app = Flask(__name__)   # instantiate Flask class to initiate the app.

def create_app():
    # initiate the flask app and database
    app.config['SECRET_KEY'] = 'Thisisthekey'   # This variable is used to securely sign cookies securely and cryptographic operations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)  # The connection string for the db that flask app will connect to
    db.init_app(app)    # initialize SQLALCHEMY extension with the Flask application

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')


    from .models import User, Hotels

    with app.app_context():
        """
        creates the database tables by creating an application context for the flask application
        The application context provides access to the application's configuration, database and
        other resources within the context of the application
        """
        db.create_all()
    
    login_manager = LoginManager()  # Instanciation of the LoginManager class that handles user authentication
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # callback function that loads a user object from user ID stored in the session
        return User.query.get(int(id))
    
    @app.context_processor
    def global_var():
        # declare global variables that will be accessible from all templates
        user=current_user
        return {'user': user}

    return app

def create_database(app):
    # create database if it doesn't exist
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
