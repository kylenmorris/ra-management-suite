import os
from flask import Flask
from flask_login import LoginManager

from extensions import db, migrate
from models import Announcement

from models import User
from views.auth import auth
from views.home import home
# from models import UserProfile

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


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/server_db'

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


# Create a function to handle user profile creation and updates
# def update_user_profile(user, first_name, last_name, birthdate, phone_number, pronouns, gender, major, address_line_1,
#                         address_line_2, postcode, city, province, shift_availability):
#     # Check if the user has an existing profile
#     profile = user.profile
#     if not profile:
#         # If the user doesn't have a profile, create one
#         profile = UserProfile(user=user, first_name=first_name, last_name=last_name, birthdate=birthdate,
#                               phone_number=phone_number, pronouns=pronouns, gender=gender, major=major,
#                               address_line_1=address_line_1, address_line_2=address_line_2, postcode=postcode,
#                               city=city, province=province, shift_availability=shift_availability)
#     else:
#         # If the user has a profile, update the fields
#         profile.first_name = first_name
#         profile.last_name = last_name
#         profile.birthdate = birthdate
#         profile.phone_number = phone_number
#         profile.pronouns = pronouns
#         profile.gender = gender
#         profile.major = major
#         profile.address_line_1 = address_line_1
#         profile.address_line_2 = address_line_2
#         profile.postcode = postcode
#         profile.city = city
#         profile.province = province
#         profile.shift_availability = shift_availability
#
#     db.session.add(profile)
#     db.session.commit()
#
#     return profile
