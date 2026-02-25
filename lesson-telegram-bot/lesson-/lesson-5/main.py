from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove #  Добавляем клавиатуру еебой
from config import TOKEN_API
from aiogram.filters import Command
import asyncio  

bot = Bot(TOKEN_API)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
#    one_time_keyboard=True, # default False после нажатия кнопки она исчезнет
    keyboard=[
        [KeyboardButton(text='/help'), KeyboardButton(text='/photo')],
        [KeyboardButton(text='/description')]
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
                           #reply_markup=ReplyKeyboardRemove()
                           )
    await message.delete()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, 
                           text='Добро пожаловать в нашего бота🎹',
                           reply_markup=kb)

@dp.message(Command('description'))
async def description_command(message: types.Message):
    await message.answer("Бот способный он может отправлять фото")

@dp.message(Command('photo'))
async def photo_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://avatars.mds.yandex.net/get-kino-vod-films-gallery/1668876/2707e757adaf9eb3f1ff3cf7b7715370/380x240")

async def on_startup():
    print('Бот запущен🪰')

async def main():
    await on_startup()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    
    asyncio.run(main())