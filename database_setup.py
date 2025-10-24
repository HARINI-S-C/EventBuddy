"""
database_setup.py
-----------------
Handles PostgreSQL connection setup using SQLAlchemy and psycopg2.
Reads credentials from environment variables for security.
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

# --- Database Configuration ---
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "require")

# --- Validate Required Variables ---
required_vars = [POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB]
if not all(required_vars):
    print("❌ Missing one or more required PostgreSQL environment variables.")
    sys.exit(1)

# --- Test psycopg2 Connection (Optional but Useful) ---
try:
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        sslmode=POSTGRES_SSLMODE
    )
    print("✅ Connected successfully to PostgreSQL (psycopg2 test).")
    conn.close()
except Exception as e:
    print("❌ PostgreSQL connection test failed:", e)
    sys.exit(1)

# --- Build SQLAlchemy DATABASE_URL ---
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    f"?sslmode={POSTGRES_SSLMODE}"
)

# --- SQLAlchemy Engine and Session ---
try:
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base = declarative_base()
    print("✅ SQLAlchemy engine created successfully.")
except Exception as e:
    print("❌ Error creating SQLAlchemy engine:", e)
    sys.exit(1)
