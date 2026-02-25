from aiogram import Bot, Dispatcher, types
import asyncio
from config import TOKEN_API
from aiogram.filters import Command

bot = Bot(TOKEN_API)
dp = Dispatcher()

HELP_COMMAND = """
/help - <em>ты че дурак штоле?</em>
<b>/give</b> - <em>хайпануть</em>
"""

async def on_startup():
    print("Система работает в штатном режиме")

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND, parse_mode='HTML')

@dp.message(Command('give'))
async def give_comamnd(message: types.Message):
    await message.answer("Смотри какой ты смешной))) 🖕🏿🖕🏿🖕🏿🖕🏿")
    await bot.send_sticker(message.from_user.id, sticker = "CAACAgIAAxkBAAEP_fFpPUVI1hiI8IZ6uoqMwH52u99T6gAC3hIAAmdBmEhnB6oIFzDwtzYE")
    await message.delete()


@dp.message()
async def count_galka(message: types.Message):
    
    if message.sticker:
        sticker_id = message.sticker.file_id
        await message.answer(f"Эта залупа иммет такой ID: {sticker_id}")
    else:
        count = message.text.count('👩‍🦽')
        await message.answer(f'{count}')

#@dp.message()
async def heart_echo(message: types.Message):

    if message.text == '👩‍🦽':
        await message.answer('🏃')
    else:
        await message.answer(message.text)

async def main():
    print("Система работает в штатном режиме")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())