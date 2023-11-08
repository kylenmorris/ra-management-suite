from models import User
# from models import UserProfile
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort

# from RAManagementSuite.models import UserProfile


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(first_name, last_name, email, password):
    hashed_password = generate_password_hash(password)
    user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()


# Additional user operations can go here...

# def create_user_profile(user_id, first_name, last_name, birthdate, phone_number, pronouns, gender, major,
#                         address_line_1, address_line_2, postcode, city, province, shift_availability):
#     profile = UserProfile(
#         user_id=user_id,
#         first_name=first_name,
#         last_name=last_name,
#         birthdate=birthdate,
#         phone_number=phone_number,
#         pronouns=pronouns,
#         gender=gender,
#         major=major,
#         address_line_1=address_line_1,
#         address_line_2=address_line_2,
#         postcode=postcode,
#         city=city,
#         province=province,
#         shift_availability=shift_availability
#     )
#     db.session.add(profile)
#     db.session.commit()
