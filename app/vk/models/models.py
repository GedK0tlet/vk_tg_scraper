from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database.database import Base

class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    host_group = Column(String, index=True)

class PostsGroup(Base):
    __tablename__ = 'posts_group'

    id = Column(Integer, primary_key=True, index=True)
    text_post = Column(String, index=True)
    post_id = Column(String, index=True)
    host_post_id = Column(Integer, ForeignKey('groups.id'))

class CommentsGroups(Base):
    __tablename__ = 'comments_groups'

    id = Column(Integer, primary_key=True, index=True)
    text_comment = Column(String, index=True)
    id_user = Column(String, index = True)
    post_id_vk = Column(String, index = True)

