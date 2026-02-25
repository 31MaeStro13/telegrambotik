from config import TOKEN_API 
import asyncio
from aiogram import Bot, Dispatcher, types 
from aiogram.filters import Command
import random

bot = Bot(TOKEN_API)
dp = Dispatcher()

alphabet = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'         
)

count = 0 

HELP_COMMAND = '''
/help - список команд
/start - запустить бота
/description - описание бота
/count - количество собственных вызовов 
'''

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(text="Добро пожаловать в наш телеграмм бот!")
    await message.delete()

@dp.message(Command('description'))
async def description_command(message: types.Message):
    await message.answer(text="работаю по тихонечку")

@dp.message(Command('count'))
async def count_command(message: types.Message):
    global count
    count += 1
    await message.reply(text=f'Меня использовали {count} раз')

@dp.message()
async def echo(message: types.Message):
    if '0' in message.text:
        await message.answer("YES")
    else:
        await message.answer("NO")
    await message.answer(random.choice(alphabet))



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':

    asyncio.run(main())