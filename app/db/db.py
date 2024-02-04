from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.constants import SQL_DATABASE_URL

engine = create_engine(SQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
