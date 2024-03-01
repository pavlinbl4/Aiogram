# pip install python-dotenv
from aiogram import Bot, Dispatcher
import asyncio

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

from utils.commands import set_commands
from handlers.start import get_start
from aiogram.filters import Command

load_dotenv()
token = os.getenv('crazypythonbot')
admin_id = os.getenv('channel_id')

# Replace 'HTML' with your desired parse_mode, if applicable
bot_properties = DefaultBotProperties(parse_mode='HTML')

bot = Bot(token=token, default=bot_properties)
dp = Dispatcher()


async def start_bot(bot: Bot):
    await bot.send_message(admin_id, text='I am working')


dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))


async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
