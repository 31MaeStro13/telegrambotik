from aiogram import Bot, Dispatcher, types
from config import TOKEN_API
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
import asyncio

bot = Bot(TOKEN_API)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(text='/help')],
        [KeyboardButton(text='/description'), KeyboardButton(text='💍')]
    ]
)

HELP_COMMAND = """
<b>/start</b> - <em>запустить ботика</em>
<b>/help</b> - <em>список команд</em>
<b>/description</b> - <em>описание бота</em>
<b>/photo</b> - <em>отправка фото</em>
"""

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, 
                           text=HELP_COMMAND,
                           parse_mode='HTML',
                           )
    await message.delete()

@dp.message(Command('start'))
async def desc_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='you botik',
                           reply_markup=kb
                           )
    await message.delete()


@dp.message(Command('description'))
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, 
                           text='пока ничего не могу',
                           parse_mode='HTML',
                           )
    await message.delete()

@dp.message()
async def echo(message: types.Message):
    if message.text == '💍':
        await bot.send_photo(chat_id=message.chat.id,
                         photo="https://avatars.mds.yandex.net/get-kino-vod-films-gallery/1668876/2707e757adaf9eb3f1ff3cf7b7715370/380x240"
                         )

async def on_startup():
    print('Бот запущен🪰')

async def main():
    await on_startup()
    await dp.start_polling(bot, skip_update=True)

if __name__ == "__main__":
    asyncio.run(main())