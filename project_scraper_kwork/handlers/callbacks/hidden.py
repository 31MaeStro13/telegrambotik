from aiogram import Router, F
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON
import service.db_service as db_service

hidden_router = Router()

@hidden_router.callback_query(F.data.startswith('hide_'))
async def hide_project(callback: CallbackQuery):
    project_id = callback.data.replace('hide_', '')
    user_id = callback.from_user.id

    success = db_service.add_to_hidden(user_id, project_id)

    if success:
        await callback.answer(LEXICON["success_hide"])
        await callback.message.delete()
    else:
        await callback.answer(LEXICON["error_hide"], show_alert=True)


@hidden_router.callback_query(F.data.startswith('restore_'))
async def restore_project(callback: CallbackQuery):
    project_id = callback.data.replace('restore_', '')
    user_id = callback.from_user.id

    success = db_service.remove_from_hidden(user_id, project_id)

    if success:
        await callback.answer(LEXICON["success_restore"])
        await callback.message.delete()
    else:
        await callback.answer(LEXICON["error_restore"], show_alert=True)