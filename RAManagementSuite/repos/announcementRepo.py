from RAManagementSuite.models import Announcement
from RAManagementSuite.extensions import db
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
