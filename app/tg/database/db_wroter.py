from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from models.models_db import *
from contextlib import contextmanager


def wrote(data):
    ...
