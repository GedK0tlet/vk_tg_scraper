from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO: create secret data
DATABASE_NAME = "TG"

URL_DATABASE = f'postgresql://postgres:Gozime32@localhost:5438/{DATABASE_NAME}'

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()