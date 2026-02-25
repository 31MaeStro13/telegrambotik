from config import TOKEN_API
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio


HELP_COMMAND = """
/help - список команд
/start - запустить бота
"""

bot=Bot(TOKEN_API)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(text="Добро пожаловать в наш телеграмм бот!")
    await message.delete()

@dp.message()
async def echo(message: types.Message):
    await message.answer(f'Вы сказали {message.text}')

if __name__ == '__main__':

    asyncio.run(main())