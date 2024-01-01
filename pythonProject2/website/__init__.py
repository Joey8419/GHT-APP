from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize Flask-SqlAlchemy
db = SQLAlchemy()
DB_NAME = "Outbreaks.db"


# Define a function:
def create_app():
    # This is how flask is initialized; __name__ represents the name of the file that was run:
    app = Flask(__name__)
    # config variable encrypts and secures the cookies and session data related to the website:
    app.config['SECRET_KEY'] = 'GHT APP'
    # Storing database inside website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Taking database and telling it which app to use
    db.init_app(app)

    # Blueprints must be registered in this file:
    from .views import views
    from .auth import auth
    from .load_data import load_data

    # Register the blueprints:
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(load_data)


    # Import db after initializing it
    from .model import User, Outbreaks, Search

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Uses function to load user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
