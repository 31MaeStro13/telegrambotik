from aiogram import Bot, Dispatcher, types
import asyncio

TOKEN_API = "8023808359:AAG5zTPjmaBqaFoXqjKP3ywCZHyhfVVQaeE"

bot = Bot(TOKEN_API)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(text = message.text) # написать сообщение

async def main():  # Добавил
    await dp.start_polling(bot)


if __name__ == '__main__':

    asyncio.run(main()) 

    