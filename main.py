from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_setup import SessionLocal, Base, engine
import models, schemas, crud, auth
from passlib.context import CryptContext
from jose import JWTError

# ---------------------- Initialize App ----------------------
app = FastAPI(
    title="🎟️ EventBuddy API",
    description="Event management and RSVP system",
    version="1.0"
)

# ---------------------- Password Hashing ----------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------- Database Dependency ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- Users Endpoints ----------------------
@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user with hashed password"""
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    return crud.create_user(db, user.name, user.email, hashed_pw)


@app.get("/users/", response_model=list[schemas.UserRead])
def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    return db.query(models.User).all()


# ---------------------- Events Endpoints ----------------------
@app.post("/events/", response_model=schemas.EventRead)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    return crud.create_event(db, event.title, event.description, event.max_seats)


@app.get("/events/", response_model=list[schemas.EventRead])
def get_events(db: Session = Depends(get_db)):
    """Get all events"""
    return db.query(models.Event).all()


# ---------------------- RSVP Endpoints ----------------------
@app.post("/rsvps/")
def create_rsvp(rsvp: schemas.RSVPCreate, db: Session = Depends(get_db)):
    """RSVP to an event"""
    return crud.create_rsvp(db, rsvp.user_id, rsvp.event_id)


# ---------------------- Auth / Login ----------------------
@app.post("/token", response_model=schemas.Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login and generate JWT token"""
    user = crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------- Authenticated User Example ----------------------
def get_current_user(token: str = Depends(auth.verify_access_token), db: Session = Depends(get_db)):
    try:
        payload = auth.verify_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = crud.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
