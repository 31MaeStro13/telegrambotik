from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON
from handlers.profile import ProfileStates

profile_callback_router = Router()

@profile_callback_router.callback_query(F.data == "edit_profile")
async def process_edit_profile_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LEXICON["profile_ask_stack"])
    await state.set_state(ProfileStates.stack)
    await callback.answer()