import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from get_credentials import Credentials

TOKEN = Credentials().pavlinbl4_bot

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


# Define a list of allowed user IDs
# allowed_user_ids = {123456789, 987654321, 1237220337}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    # await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    # await message.answer(f"Your id, {hbold(message.from_user.id)}!")


@dp.message(F.from_user.id.in_({187597961}))
async def handle_allowed_user_messages(message: types.Message):
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
                         f"you are allowed user!")

    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """


@dp.message()
async def handle_other_messages(message: types.Message):
    # This function will be called for messages from any other user
    await message.reply("Sorry, you are not an allowed user.")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
