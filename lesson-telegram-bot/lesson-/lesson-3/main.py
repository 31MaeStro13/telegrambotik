from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher()

async def on_startup():
    print('Бот запущен')


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('<em>Ку че <b>хипуешь???</b></em>', parse_mode='HTML')  # Это parse_mod необязатльный параметр как например end и sed в print, тут он отвечает за формат сообщения
    await message.delete()

@dp.message(Command('give'))
async def give_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEP_dtpPSB4hATm5QbGvW1uFMBK1j8AAa0AAs4TAAJBSJhISFmTQ7WzDgABNgQ")  #  Чтобы узнать id стикера можно написать телеграмм боту
    await message.delete()

@dp.message()
async def send_emoji(message: types.Message):
    await message.reply(message.text + '🫥')

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())