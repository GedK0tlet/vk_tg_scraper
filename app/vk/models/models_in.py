from pydantic import BaseModel
from typing import List

class UsersPageBase(BaseModel):
    vk_id_user: str

class GroupPageBase(BaseModel):
    host_group: str


class PostBase(BaseModel):
    post_id_vk: str
    text_post: str
    host_post_id: int

class CommentBase(BaseModel):
    text_comment: str
    post_id: int
    id_user: str

class PostComBase(PostBase):
    comments: List[CommentBase]