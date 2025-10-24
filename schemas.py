from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# -------------------- USER SCHEMAS --------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enables ORM -> Pydantic conversion


# -------------------- EVENT SCHEMAS --------------------
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    max_seats: int


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------- RSVP SCHEMAS --------------------
class RSVPBase(BaseModel):
    user_id: int
    event_id: int


class RSVPCreate(RSVPBase):
    pass


class RSVPRead(RSVPBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------- AUTH TOKEN --------------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
