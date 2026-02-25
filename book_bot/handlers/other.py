from aiogram import Router
from aiogram.types import Message

other_router = Router()

@other_router.message()
async def other_process_message(message: Message):
    await message.answer(f"Это эхо! {message.text}")