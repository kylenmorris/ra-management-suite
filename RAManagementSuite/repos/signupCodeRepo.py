from models import SignupCode
from extensions import db
from werkzeug.exceptions import abort


def get_signup_code(signup_code):
    code = SignupCode.query.filter_by(code=signup_code).first()
    return code


def get_signup_codes():
    return SignupCode.query.all()


def create_signup_code(code):
    code = SignupCode(code=code)
    db.session.add(code)
    db.session.commit()


def edit_signup_code(id, used):
    code = SignupCode.query.filter_by(id=id).first()
    if code:
        code.used = used
        db.session.commit()


# def del_announcement(id):
#     try:
#         announcement = Announcement.query.get(id)
#         if announcement:
#             db.session.delete(announcement)
#             db.session.commit()
#             return True  # Return a success indicator
#         else:
#             return False  # Return a failure indicator (announcement not found)
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         db.session.rollback()
#         return False  # Return a failure indicator





