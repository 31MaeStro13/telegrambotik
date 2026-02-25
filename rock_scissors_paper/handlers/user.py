from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from keyboard.keyboard import yes_no_kb, game_kb
from service.service import get_bot_choice, get_winner

user_router = Router()

@user_router.message(CommandStart())
async def command_start_process(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=yes_no_kb)

@user_router.message(Command('help'))
async def command_help_process(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         reply_markup=yes_no_kb)

@user_router.message(F.text == LEXICON_RU['yes_button'])
async def yes_button_process(message: Message):
    await message.answer(text=LEXICON_RU['yes'],
                         reply_markup=game_kb)

@user_router.message(F.text == LEXICON_RU['no_button'])
async def no_button_process(message: Message):
    await message.answer(text=LEXICON_RU['no'])


@user_router.message(
    F.text.in_([LEXICON_RU["rock"], LEXICON_RU["paper"], LEXICON_RU["scissors"]])
)
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f"{LEXICON_RU['bot_choice']} - {LEXICON_RU[bot_choice]}")
    winner = get_winner(message.text, bot_choice)

    if winner == "user_won":
        message_effect_id = "5046509860389126442"
    else:
        message_effect_id = None

    await message.answer(
        text=LEXICON_RU[winner],
        message_effect_id=message_effect_id,
        reply_markup=yes_no_kb,
    )
