import os
from flask import Flask
from flask_login import LoginManager

from extensions import db, migrate
from models import Announcement, SignupCode

from models import User
from views.auth import auth
from views.home import home

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def initialize_database():
    # Check if the table is empty
    if not Announcement.query.first():
        initial_announcements = [
            Announcement(title='First Announcement', content='Content for the first announcement.html'),
            Announcement(title='Second Announcement', content='Content for the second announcement.html')
        ]
        for ann in initial_announcements:
            db.session.add(ann)
        db.session.commit()

    if not SignupCode.query.first():
        initial_signup_codes = [
            SignupCode(code=1234),
            SignupCode(code=1111)
        ]
        for code in initial_signup_codes:
            db.session.add(code)
        db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/server_db'

    db.init_app(app)
    migrate.init_app(app, db)  # for quickly changing the db

    app.register_blueprint(auth)
    app.register_blueprint(home)

    with app.app_context():
        db.create_all()  # this creates all tables based on the models defined
        initialize_database()  # this will populate the database with initial data

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
