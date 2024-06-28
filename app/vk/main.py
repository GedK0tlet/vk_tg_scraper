from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from sqlalchemy.orm import Session
from models import models
from models.models_in import *
from database import database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:3000",
]

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/add_group/")
async def add_group(user_id: GroupPageBase, db: db_dependency, skip: int = 0, limit = 100):
    groups = db.query(models.Groups).offset(skip).limit(limit).all()
    flag = False
    for group in groups:
        if group.host_group == user_id.host_group:
            flag = True
    if not flag:
        db_group = models.Groups(host_group=user_id.host_group)
        db.add(db_group)
        db.commit()

@app.post("/add_user/")
async def add_user(user_id: UsersPageBase, db: db_dependency, skip: int = 0, limit = 100):
    users = db.query(models.UserPages).offset(skip).limit(limit).all()
    flag = False
    for user in users:
        if user.vk_id_user == user_id.vk_id_user:
            flag = True
    if not flag:
        db_user = models.UserPages(vk_id_user=user_id.vk_id_user)
        db.add(db_user)
        db.commit()

@app.get("/show_users/")
async def show_users_list(db: db_dependency, skip: int = 0, limit: int = 100):
    groups = db.query(models.UserPages).offset(skip).limit(limit).all()
    
    return groups

@app.get("/vk_groups/")
async def show_list_groups(db: db_dependency, skip: int = 0, limit: int = 100):
    groups = db.query(models.Groups).offset(skip).limit(limit).all()
    print(groups)
    return groups