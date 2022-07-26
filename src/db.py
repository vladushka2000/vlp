from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import os

db_user = os.getenv("DB_USER", "vlp")
db_pass = os.getenv("DB_PASS", "vlp")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/vlp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)


def get_session():
    return Session(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
