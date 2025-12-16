from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config.py import TOKEN_API # type: ignore

bot = Bot(TOKEN_API)
dp = Dispatcher()

@dp.message()
def echo(message: Message.types):
    message.answer(text=message.text())


if __name__ == "__main__":
    dp.run_polling()