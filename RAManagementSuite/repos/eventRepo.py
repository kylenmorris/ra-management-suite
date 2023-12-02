from datetime import datetime
from models import Event
from extensions import db

from models import Event, EventType
from extensions import db


def create_event(title, start_date, end_date, owner_id, color, description,
                 event_type=EventType.NORMAL, assigned_user_id=None):
    # Convert string dates to datetime objects
    start_date_object = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
    end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

    event = Event(title=title,
                  start_date=start_date_object,
                  end_date=end_date_object,
                  owner_id=owner_id,
                  color=color,
                  description=description,
                  event_type=event_type,
                  assigned_user_id=assigned_user_id)
    db.session.add(event)
    db.session.commit()


def get_all_events():
    return Event.query.all()


def get_event_by_id(event_id):
    return Event.query.get(event_id)


def update_event(event_id, title, start_date, end_date, color, description,
                 event_type=None, assigned_user_id=None):
    event = get_event_by_id(event_id)
    if event:
        event.title = title
        event.start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        event.end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        event.color = color
        event.description = description
        event.assigned_user_id = assigned_user_id
        if event_type is not None:
            event.event_type = event_type
        db.session.commit()
    else:
        raise ValueError("Event not found")


def delete_event(event_id):
    event = get_event_by_id(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    else:
        raise ValueError("Event not found")
