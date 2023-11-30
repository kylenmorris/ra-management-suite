import os
from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from extensions import db, migrate
from models import Announcement, SignupCode

from models import User
from repos import userRepo
from views.event import event
from views.profile import profile
from views.code import code
from views.task import task
from views.auth import auth
from views.home import home
from views.user import user
from views.announcement import announcement

from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def initialize_database():
    # Check if the table is empty
    if not Announcement.query.first():
        initial_announcements = [
            Announcement(title='First Announcement', content='Content for the first index.html'),
            Announcement(title='Second Announcement', content='Content for the second index.html')
        ]
        for ann in initial_announcements:
            db.session.add(ann)
        db.session.commit()

    if not SignupCode.query.first():
        expired_date = datetime.today() - timedelta(days=8)

        initial_signup_codes = [
            SignupCode(code=1234),
            SignupCode(code=9999, used=True),
            SignupCode(code=1001, created=expired_date)
        ]
        for code in initial_signup_codes:
            db.session.add(code)
        db.session.commit()

    if not userRepo.get_user_by_email("coordinator@test.com"):
        hashed_password = generate_password_hash("password")
        db.session.add(User(name="coordinator", email="coordinator@test.com", password=hashed_password, role="COORDINATOR"))
        db.session.commit()

    if not userRepo.get_user_by_email("senior@test.com"):
        hashed_password = generate_password_hash("password")
        db.session.add(User(name="senior", email="senior@test.com", password=hashed_password, role="SENIOR"))
        db.session.commit()

    if not userRepo.get_user_by_email("returner@test.com"):
        hashed_password = generate_password_hash("password")
        db.session.add(User(name="admin", email="returner@test.com", password=hashed_password, role="RETURNER"))
        db.session.commit()

    if not userRepo.get_user_by_email("basic@test.com"):
        hashed_password = generate_password_hash("password")
        db.session.add(User(name="basic", email="basic@test.com", password=hashed_password, role="BASIC"))
        db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/server_db'

    db.init_app(app)
    migrate.init_app(app, db)  # for quickly changing the db

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(task, url_prefix='/task')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(announcement, url_prefix='/announcement')
    app.register_blueprint(code, url_prefix='/code')
    app.register_blueprint(event, url_prefix='/event')
    app.register_blueprint(user, url_prefix='/user')

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
