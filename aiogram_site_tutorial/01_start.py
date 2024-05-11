import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from get_credentials import Credentials

TOKEN = Credentials().pavlinbl4_bot

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Define a list of allowed user IDs
allowed_user_ids: set[int] = {123456789, 987654321, 1237220337, 187597961}
"""
This handler receives messages with `/start` command
"""


@dp.message(CommandStart())
async def command_start_handler() -> None:


@dp.message(F.from_user.id.in_(allowed_user_ids))
async def handle_allowed_user_messages(message: types.Message):
    photo_id = message.photo[-1].file_id

    file = await bot.get_file(photo_id)
    file_path = file.file_path

    await bot.download_file(file_path, f"../DownloadedFiles/{photo_id}.jpg")

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}\n"
                         f"your id - {message.from_user.id}\n"
                         f"your username - {message.from_user.username}\n"
                         f"your first name - {message.from_user.first_name}\n"
                         f"your last name - {message.from_user.last_name}\n"
                         f"your added to attachment menu - {message.from_user.added_to_attachment_menu}\n"
                         f"your premium - {message.from_user.is_premium}\n"
                         f"your is bot - {message.from_user.is_bot}\n"
                         f"your url - {message.from_user.url}\n"
                         f"your language code - {message.from_user.language_code}\n"
                         f"your model config - {message.from_user.model_config}\n"
                         f"photo_id - {photo_id}\n"
                         f"file - {file_path}\n"
                         f"you are allowed user!")

    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    # try:
    #     # Send a copy of the received message
    #     await message.reply("Hello, allowed user!")
    #     await message.send_copy(chat_id=message.chat.id)
    # except TypeError:
    #     # But not all the types is supported to be copied so need to handle it
    #     await message.answer("Nice try!")


@dp.message()
async def handle_other_messages(message: types.Message):
    # This function will be called for messages from any other user
    await message.reply("Sorry, you are not an allowed user.")


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
