from datetime import datetime
from RAManagementSuite.models import Event
from RAManagementSuite.extensions import db


def create_event(title, start_date, end_date, owner_id):
    # Convert string dates to datetime objects
    start_date_object = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
    end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

    # Assuming you have an Event model, and you're adding data to it like this:
    event = Event(title=title, start_date=start_date_object, end_date=end_date_object, owner_id=owner_id)
    db.session.add(event)
    db.session.commit()


def get_all_events():
    return Event.query.all()


def get_event_by_id(event_id):
    return Event.query.get(event_id)

# ... Add more methods as required ...
