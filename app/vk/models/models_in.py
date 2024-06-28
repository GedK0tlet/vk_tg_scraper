from pydantic import BaseModel
from typing import List

class UsersPageBase(BaseModel):
    vk_id_user: str

class GroupPageBase(BaseModel):
    host_group: str