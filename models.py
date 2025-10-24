from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database_setup import Base  # from your file

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationship — one user → many RSVPs
    rsvps = relationship("RSVP", back_populates="user", cascade="all, delete")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    max_seats = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationship — one event → many RSVPs
    rsvps = relationship("RSVP", back_populates="event", cascade="all, delete")

class RSVP(Base):
    __tablename__ = "rsvps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationships (reverse mapping)
    user = relationship("User", back_populates="rsvps")
    event = relationship("Event", back_populates="rsvps")
