from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU

router_command = Router()

@router_command.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

@router_command.message(Command('help'))
async def command_help(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
