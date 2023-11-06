from models import Announcement
from extensions import db
from werkzeug.exceptions import abort


def get_announcement(announcement_id):
    announcement = Announcement.query.filter_by(id=announcement_id).first()
    if announcement is None:
        abort(404)
    return announcement


def get_announcements():
    return Announcement.query.all()


def create_announcement(title, content):
    announcement = Announcement(title=title, content=content)
    db.session.add(announcement)
    db.session.commit()


def edit_announcement(title, content, id):
    announcement = Announcement.query.filter_by(id=id).first()
    if announcement:
        announcement.title = title
        announcement.content = content
        db.session.commit()

def del_announcement(id):
    try:
        announcement = Announcement.query.get(id)
        if announcement:
            db.session.delete(announcement)
            db.session.commit()
            return True  # Return a success indicator
        else:
            return False  # Return a failure indicator (announcement not found)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db.session.rollback()
        return False  # Return a failure indicator





