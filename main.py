from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN_API = "8023808359:AAG5zTPjmaBqaFoXqjKP3ywCZHyhfVVQaeE"

bot = Bot()
dp = Dispatcher

@dp.message()
def echo(message: Message.types):
    message.answer(text=message.text())


if __name__ == "__main__":
    dp.run_polling()