from aiogram import Bot, Dispatcher, types 
from config import TOKEN_API
import asyncio
from aiogram.filters import Command

bot = Bot(TOKEN_API)
dp = Dispatcher()

HELP_COMMAND = """
<b>/help</b> - <em>дапоможити мени</em>
<b>/start</b> - <em>начинаем</em>
<b>/картинка</b> - <em>картинка не работает</em>
<b>/give</b> - <em>та же картинка тольк по английски</em>
"""

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Ехало!")



@dp.message(Command('help'))
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode='HTML')
    await message.delete()



@dp.message(Command('give'))
async def send_image(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://cdn.krut-art.ru/uploads/2018/09/prosto-prelest.jpg")
    await message.delete()

@dp.message(Command('location'))
async def send_mesto(message: types.Message):
    await bot.send_location(
        chat_id=message.chat.id,  # или message.from_user.id для ЛС
        latitude=55.7558,         # Широта (правильное название!)
        longitude=37.6173         # Долгота (правильное название!)
    )
    await message.delete()


@dp.message()
async def echo(message: types.Message):
#   await message.answer(message.text)
    await bot.send_message(chat_id=message.from_user.id, 
                           text="Hello")

async def main():
    await dp.start_polling(bot, skip_update=True)

if __name__ == "__main__":
    asyncio.run(main())