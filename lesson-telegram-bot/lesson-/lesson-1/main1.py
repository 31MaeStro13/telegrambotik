from aiogram import Bot, Dispatcher, types # type: ignore
import asyncio 
from config import TOKEN_API # type: ignore


# TOKEN_APY = "8023808359:AAG5zTPjmaBqaFoXqjKP3ywCZHyhfVVQaeE"


bot = Bot(TOKEN_API)
dp=Dispatcher()

@dp.message()
async def echo_upper(message: types.Message):
    if message.text.count(' ') >= 1:  # считаем количество пробелов
        await message.answer(text = message.text.upper())  # Перевод в верхний регистр

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())