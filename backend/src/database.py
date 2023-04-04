from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import config

engine = create_engine(config.get_alchemy_url())
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
model = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
