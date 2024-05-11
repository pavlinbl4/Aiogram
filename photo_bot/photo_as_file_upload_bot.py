import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from get_credentials import Credentials
from icecream import ic

# Configuration
TOKEN = Credentials().pavlinbl4_bot
ALLOWED_USER_IDS = {123456789, 987654321, 1237220337, 187597961}

# Initialize Bot and Dispatcher
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Я бот помогающий добавлять фотографии в архив!\n"
                         f"Отправьте фото «как файл», чтоб сохранить качество\n"
                         f"снимка"
                         )


@dp.message(F.from_user.id.in_(ALLOWED_USER_IDS))
async def handle_allowed_user_messages(message: types.Message):
    if message.document is None:
        await message.answer(f"Отправьте фото «как файл», чтоб сохранить качество\n"
                             f"снимка")
    else:
        uploaded_file = message.document
        file_id = uploaded_file.file_id
        # ic(uploaded_file)

        # get file path
        file = await bot.get_file(file_id)
        file_path = file.file_path

        allowed_files_type = {'image/jpeg',
                              'image/png',
                              }

        if uploaded_file.mime_type in allowed_files_type:

            # save file to hdd
            await bot.download_file(file_path, f"../DownloadedFiles/{uploaded_file.file_name}.jpg")

            # send message to sender
            await message.answer(f"Hello, {hbold(message.from_user.full_name)}\n"
                                 f"file_name - {uploaded_file.file_name} "
                                 f"file_id - {uploaded_file.file_id} "
                                 f"file_size - {uploaded_file.file_size}\n"
                                 f"file_type - {uploaded_file.mime_type}\n"
                                 # f"photo_id - {}\n"
                                 f"you are allowed user!")

            ic(f'path to uploading image : ../DownloadedFiles/{uploaded_file.file_name}.jpg')



        else:
            await message.answer(f"Вы отправили недопустимый тип файла - {uploaded_file.mime_type}\n"
                                 f"я работаю только с фотографиями")


@dp.message()
async def handle_other_messages(message: types.Message):
    # This function will be called for messages from any other user
    await message.reply("Sorry, you are not an allowed user.")


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
