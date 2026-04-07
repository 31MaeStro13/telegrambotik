from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def get_profile_edit_keyboard() -> InlineKeyboardMarkup:
    """Кнопка для редактирования профиля"""
    builder = InlineKeyboardBuilder()
    builder.button(text=LEXICON["profile_edit"], callback_data="edit_profile")
    builder.adjust(1)
    return builder.as_markup()


def get_experience_keyboard() -> InlineKeyboardMarkup:
    """Кнопки для выбора опыта"""
    builder = InlineKeyboardBuilder()
    builder.button(text=LEXICON["exp_0_1"], callback_data="exp_0_1")
    builder.button(text=LEXICON["exp_1_3"], callback_data="exp_1_3")
    builder.button(text=LEXICON["exp_3plus"], callback_data="exp_3plus")
    builder.adjust(1)
    return builder.as_markup()


def get_profile_confirm_keyboard() -> InlineKeyboardMarkup:
    """Кнопки подтверждения (сохранить / заново)"""
    builder = InlineKeyboardBuilder()
    builder.button(text=LEXICON["profile_confirm_yes"], callback_data="profile_save")
    builder.button(text=LEXICON["profile_confirm_no"], callback_data="profile_restart")
    builder.adjust(1)
    return builder.as_markup()