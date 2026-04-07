from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_inline_favorit_kb(project_id: str, has_more: bool = False) -> InlineKeyboardMarkup:
    """
    Простая клавиатура для одного проекта
    """
    builder = InlineKeyboardBuilder()

    # Кнопка "В избранное"
    btn_fav = InlineKeyboardButton(
        text=LEXICON['favorite'],
        callback_data=f"fav_{project_id}"
    )

    # Кнопка "Скрыть"
    btn_hide = InlineKeyboardButton(
        text=LEXICON['hide'],
        callback_data=f"hide_{project_id}"
    )

    if has_more:
        # Кнопка "Подробнее"
        btn_more = InlineKeyboardButton(
            text=LEXICON['more'],
            callback_data=f"more_{project_id}"
        )
        builder.row(btn_fav, btn_hide, btn_more, width=3)
    else:
        builder.row(btn_fav, btn_hide, width=2)

    return builder.as_markup()


def get_favorite_keyboard(project_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для проекта в избранном
    """
    builder = InlineKeyboardBuilder()

    # Кнопка удалить из избранного
    btn_remove = InlineKeyboardButton(
        text=LEXICON['del'],
        callback_data=f"remove_fav_{project_id}"
    )

    # Кнопка перейти к проекту
    btn_link = InlineKeyboardButton(
        text=LEXICON['open'],
        url=f"https://kwork.ru/projects/{project_id}/view"
    )

    builder.row(btn_remove, btn_link, width=2)
    return builder.as_markup()

def get_hidden_keyboard(project_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для скрытого проекта
    """
    builder = InlineKeyboardBuilder()

    btn_restore = InlineKeyboardButton(
        text="🔄 Восстановить",
        callback_data=f"restore_{project_id}"
    )

    builder.row(btn_restore, width=1)
    return builder.as_markup()