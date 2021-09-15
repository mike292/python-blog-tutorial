from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "helloworld"
    # configure a new database with the database name(DB_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)  # initialize the database

    # @app.route("/")
    # def home():
    #     return "Hello, This is the homepage"

    # @app.route("/profile")
    # def profile():
    #     return "This is the profile page"

    # the dot in ".<filename>" because the file is in a python package
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")  # the start of the url
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)  # Create a new database

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # if not login redirect to login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # Check if the database exist
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)  # create a database
        print("Created database!")
