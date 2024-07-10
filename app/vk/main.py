from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from sqlalchemy.orm import Session
from models import models
from models.models_in import *
from database import database
from vk_mod import vk_api_get

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

@app.get("/vk_groups/")
async def show_list_groups(db: db_dependency, skip: int = 0, limit: int = 100):
    groups = db.query(models.Groups).offset(skip).limit(limit).all()
    print(groups)
    return groups

@app.get("/vk_posts_all/")
async def all_posts_vk(db: db_dependency, skip: int = 0, limit: int = 100):
    posts = db.query(models.PostsGroup).offset(skip).limit(limit).all()

    return posts

# @app.post("/vk_posts_by_wall/")
# async def posts_by_group(id_group: GroupPageBase, db: db_dependency, skip: int = 0, limit: int = 100):
#     # gr = db.query(models.Groups).filter(models.Groups.host_group.contains(id_group.host_group)).offset(skip).limit(limit).first()
#     posts = db.query(models.PostsGroup).offset(skip).limit(limit).all() #.filter(models.PostsGroup.host_post_id.contains(gr.id))
#     ar = []
#     for post in posts:
#         comments = db.query(models.CommentsGroups).filter(models.CommentsGroups.post_id_vk.contains(post.id)).offset(skip).limit(limit).all()
#         pos = PostComBase(
#             post_id_vk = post.post_id_vk,
#             text_post = post.text_post,
#             host_post_id = post.host_post_id,
#             comments = comments
#         )
#         ar.append(pos)
    
#     result: List[PostComBase] = ar

#     return result

@app.post("/update_data/")
async def update_data(db: db_dependency, skip: int = 0, limit: int = 100):
    groups = db.query(models.Groups).offset(skip).limit(limit).all()

    for group in groups:
        flag = False
        posts, comments = vk_api_get.wall_get(group.host_group, 10)
        if posts == []:
            pass
        else:
            for post in posts:
                posts_in_db = db.query(models.PostsGroup).filter(models.PostsGroup.post_id.contains(post[1])).offset(skip).limit(10).all() # must change it
                if len(posts_in_db) == 0:
                    flag = True
                
                if flag:
                    db_post = models.PostsGroup(
                        text_post = post[0],
                        post_id = post[1],
                        host_post_id = group.id
                        )
                    db.add(db_post)
                    db.commit()
            for comment in comments[0]:
                com_in_db = db.query(models.CommentsGroups).filter(models.CommentsGroups.post_id_vk.contains(comment[2])).offset(skip).limit(100).all() # must change it
                if len(com_in_db) == 0:
                    flag = True
                
                if flag:
                    db_comment = models.CommentsGroups(
                        text_comment = comment[0],
                        post_id_vk = comment[2],
                        id_user = str(f"id{comment[1]}")
                    )
                    db.add(db_comment)
                    db.commit()