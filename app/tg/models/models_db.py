from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database.database import Base

class Channels(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key = True, index = True)
    id_channel = Column(String, index = True)
    name_channel = Column(String, index = True)

class PostChannel(Base):
    __tablename__ = 'post_channel'

    id = Column(Integer, primary_key = True, index = True)
    date = Column(String, index = True)
    sendler = Column(String, index = True)
    text = Column(String, index = True)
    photo = Column(String, index = True)
    video = Column(String, index = True)
    message_id = Column(String, index = True)
    channel_post_id = Column(Integer, ForeignKey('channels.id'))
