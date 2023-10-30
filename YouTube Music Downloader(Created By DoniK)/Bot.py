import requests
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging

from sqlite import Database

bot = Bot(token='6616206659:AAGxM9ShH1ZsdOcyKKwVmlrW7_85zUfJKF0') # Tokeningizni kiritasiz QO'SHTIRNOQLARGA TEGMASDAN
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('data.db') #tegilmasin

logging.basicConfig(level=logging.INFO)

"""
    Dasturchi: DoniK (Python & Java dasturchisi)
    Telegram: https://t.me/azodov_001
    Github: https://github.com/azodov
"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Assalom alaykum menga video linkni yuboring...')
    db.create_database()
    try:
        db.add_user(message.from_user.id)
    except:
        pass


@dp.message_handler(state='*')
async def echo(message: types.Message, state: FSMContext):
    global msg_for_del, r
    try:
        bot_username = (await bot.me).username
        r = requests.post("https://yt1s.com/api/ajaxSearch/index", data={'q': message.text, 'vt': 'home'}).json()
        if db.get_file(vid=r['vid']) is None:
            convert = requests.post(
                "https://yt1s.com/api/ajaxConvert/convert",
                data={
                    'vid': r['vid'],
                    'k': r['links']['mp3']['mp3128']['k']
                }
            ).json()
            link = convert['dlink'].replace('https://', 'http://')
            msg_for_del = await message.reply(f'⏳')
            file = requests.get(link, stream=True)
            try:
                os.mkdir('audio')
            except:
                pass
            with open(f'audio/{r["vid"]}.mp3', 'wb') as f:
                for chunk in file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            with open(f'audio/{r["vid"]}.mp3', 'rb') as f:
                file_id = await message.reply_audio(open(f'audio/{r["vid"]}.mp3', 'rb'), title=convert['title'], caption=f'@{bot_username}')
            os.remove(f'audio/{r["vid"]}.mp3')
            await bot.delete_message(message.chat.id, msg_for_del.message_id)
            db.add_file(vid=r['vid'], file_id=file_id.audio.file_id)
        else:
            file_id = db.get_file(vid=r['vid'])[0]
            await message.reply_audio(file_id, caption=f'@{bot_username}')
    except Exception as e:
        print(e)
        try:
            os.remove(f'audio/{r["vid"]}.mp3')
            await bot.delete_message(message.chat.id, msg_for_del.message_id)
        except:
            pass
        await message.reply('Bu videoni yuklashni iloji bolmadi...')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
