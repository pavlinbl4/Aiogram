from aiogram import Bot
from aiogram.types import Message
from keyboads.registra_kb import register_keyboard


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Hello do you want a glass of beer?",reply_markup=register_keyboard)