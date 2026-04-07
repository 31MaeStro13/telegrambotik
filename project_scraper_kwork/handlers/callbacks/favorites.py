from aiogram import Router, F
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON
import service.db_service as db_service

fav_router = Router()

@fav_router.callback_query(F.data.startswith('fav_'))
async def add_favorite(callback: CallbackQuery):
    project_id = callback.data.replace('fav_', '')
    user_id = callback.from_user.id

    project = db_service.get_project_by_id(project_id)

    if not project:
        await callback.answer(LEXICON["error_no_project"], show_alert=True)
        return

    success = db_service.add_to_favorites(
        user_id=user_id,
        project_id=project_id,
        name=project['name'],
        price=project['price'],
        description=project['description'],
        link=project['link']
    )

    if success:
        await callback.answer(LEXICON["success_add_favorite"])
    else:
        await callback.answer(LEXICON["error_already_favorite"], show_alert=True)


@fav_router.callback_query(F.data.startswith('remove_fav_'))
async def delete_favorite(callback: CallbackQuery):
    project_id = callback.data.replace('remove_fav_', '')
    user_id = callback.from_user.id

    success = db_service.remove_from_favorites(user_id, project_id)

    if success:
        await callback.answer(LEXICON["success_remove_favorite"])
        await callback.message.delete()
    else:
        await callback.answer(LEXICON["error_remove_favorite"], show_alert=True)