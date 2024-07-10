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

bot = Bot(token=api)
dp = Dispatcher()

generate_name_img = lambda: f'IMG-{datetime.now():%Y-%m-%d-%H-%M-%S-%f}.jpg'
generate_name_vid = lambda: f'VID-{datetime.now():%Y-%m-%d-%H-%M-%S-%f}.mp4'

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Bot is worker")

@dp.message(F.text)
async def rashod_text(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    text_msg = message.text
    print(f'id - {user_id}\nfull name - {user_full_name}\nmessage - {text_msg}')
    message.answer("s")

@dp.message(F.content_type == ContentType.PHOTO)
async def rashod(message: types.Message):
    photo_info = message.photo[-1]
    photo_file = await bot.get_file(photo_info.file_id) 
    photo_url = f'https://api.telegram.org/file/bot{api}/{photo_file.file_path}' 

    img_data = requests.get(photo_url).content
    name_img = generate_name_img()
    path_file = f"/Users/evgenii/Desktop/Develop/Dev/vk_tg_scraper/app/tg/mediacontent/imgs{name_img}"

    with open(path_file, "wb") as img:
        img.write(img_data)
    text_msg = message.caption
    print(text_msg)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
