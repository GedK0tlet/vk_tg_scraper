import asyncio
import requests
from aiogram import Bot, types, Dispatcher
from aiogram import F
from sys import argv
import requests
from aiogram.filters.command import Command
from aiogram.types import ContentType
import os
from random import randint
from aiogram.types.input_file import FSInputFile
from datetime import datetime
from settings.settings_bot import *
from models.models import MessageDataChannel
from models import models_db
from database import database
from database.db_wroter import wrote

bot = Bot(token=api)
dp = Dispatcher()

models_db.Base.metadata.create_all(bind=database.engine)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Bot started")

@dp.channel_post()
async def channel_message(message: types.MessageOriginChannel):
    message_data = MessageDataChannel()

    message_data.date = message.date
    message_data.titile = message.chat.title
    message_data.username = message.chat.username
    message_data.text = message.text
    message_data.media_group_id = message.media_group_id
    message_data.photo = message.photo
    message_data.chat_id = message.chat.id
    message_data.message_id = message.message_id
    message_data.video = message.video

    print(message_data)
    wrote(message_data)




async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
