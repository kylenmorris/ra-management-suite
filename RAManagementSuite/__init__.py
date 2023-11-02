from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

db = SQLAlchemy()  # Initialize SQLAlchemy
migrate = Migrate()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH

    db.init_app(app)
    migrate.init_app(app, db)  # for quickly changing the db

    from RAManagementSuite.views.auth import auth
    app.register_blueprint(auth)

    from RAManagementSuite.views.home import home
    app.register_blueprint(home)

    return app
