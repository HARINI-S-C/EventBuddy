from database_setup import Base, engine
from models import User, Event, RSVP

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully.")
