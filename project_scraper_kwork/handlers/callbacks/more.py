from aiogram import Router, F
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON
from keyboard.favorit_kb import create_inline_favorit_kb
import service.db_service as db_service
from service.service import clean_price

more_router = Router()

@more_router.callback_query(F.data.startswith('more_'))
async def show_more(callback: CallbackQuery):
    project_id = callback.data.replace('more_', '')

    project = db_service.get_project_by_id(project_id)
    if not project:
        await callback.answer(LEXICON["error_no_project"], show_alert=True)
        return

    clean_price_text = clean_price(project['price'])

    text = LEXICON["full_description_template"].format(
        name=project['name'],
        price=clean_price_text,
        description=project['description'],
        link=project['link']
    )

    new_keyboard = create_inline_favorit_kb(
        project_id=project_id,
        has_more=False
    )

    await callback.message.edit_text(
        text=text,
        parse_mode='Markdown',
        reply_markup=new_keyboard
    )

    await callback.answer()