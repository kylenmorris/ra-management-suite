from datetime import datetime
from RAManagementSuite.models import Event
from RAManagementSuite.extensions import db


def create_event(title, start_date, end_date, owner_id, color, description):
    # Convert string dates to datetime objects
    start_date_object = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
    end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

    # Assuming you have an Event model, and you're adding data to it like this:
    event = Event(title=title,
                  start_date=start_date_object,
                  end_date=end_date_object,
                  owner_id=owner_id,
                  color=color,
                  description=description)
    db.session.add(event)
    db.session.commit()


def get_all_events():
    return Event.query.all()


def get_event_by_id(event_id):
    return Event.query.get(event_id)


def update_event(event_id, title, start_date, end_date, color, description):
    event = get_event_by_id(event_id)
    if event:
        event.title = title
        event.start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")  # Adjust the format if needed
        event.end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")  # Adjust the format if needed
        event.color = color
        event.description = description
        db.session.commit()
    else:
        raise ValueError("Event not found")
# ... Add more methods as required ...
