from sqlalchemy.orm import Session
import models, schemas

# ---------------------- USERS ----------------------
def get_user_by_email(db: Session, email: str):
    """Fetch a single user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, name: str, email: str, password: str):
    """Create a new user"""
    new_user = models.User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int):
    """Fetch user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------------------- EVENTS ----------------------
def create_event(db: Session, title: str, description: str | None, max_seats: int):
    """Create a new event"""
    new_event = models.Event(title=title, description=description, max_seats=max_seats)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


def get_event(db: Session, event_id: int):
    """Fetch event by ID"""
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def list_events(db: Session):
    """Get all events"""
    return db.query(models.Event).all()


# ---------------------- RSVPs ----------------------
def create_rsvp(db: Session, user_id: int, event_id: int):
    """RSVP to an event"""
    # Check if user and event exist
    user = get_user(db, user_id)
    event = get_event(db, event_id)

    if not user:
        raise ValueError(f"User with id {user_id} does not exist")
    if not event:
        raise ValueError(f"Event with id {event_id} does not exist")

    # Check if event is already full
    rsvp_count = db.query(models.RSVP).filter(models.RSVP.event_id == event_id).count()
    if rsvp_count >= event.max_seats:
        raise ValueError(f"Event '{event.title}' is already full")

    # Check if user already RSVPed
    existing_rsvp = (
        db.query(models.RSVP)
        .filter(models.RSVP.user_id == user_id, models.RSVP.event_id == event_id)
        .first()
    )
    if existing_rsvp:
        raise ValueError(f"User '{user.name}' has already RSVPed to event '{event.title}'")

    # Create RSVP
    new_rsvp = models.RSVP(user_id=user_id, event_id=event_id)
    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)
    return new_rsvp


def list_rsvps(db: Session, event_id: int):
    """Get all RSVPs for a given event"""
    return db.query(models.RSVP).filter(models.RSVP.event_id == event_id).all()
