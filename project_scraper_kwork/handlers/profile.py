from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from lexicon.lexicon import LEXICON
import service.db_service as db_service
from keyboard.profile_kb import (
    get_experience_keyboard,
    get_profile_confirm_keyboard
)

profile_router = Router()


class ProfileStates(StatesGroup):
    stack = State()          # какой стек?
    experience = State()     # сколько опыта?
    goals = State()          # какие цели?
    confirm = State()        # подтверждение


# ============================================
# ШАГ 1: СТЕК
# ============================================
@profile_router.message(StateFilter(ProfileStates.stack))
async def process_stack(message: Message, state: FSMContext):
    stack_text = message.text.strip()

    if len(stack_text) < 3:
        await message.answer("❌ Слишком коротко. Опишите ваш стек подробнее:")
        return

    await state.update_data(stack=stack_text)

    await message.answer(
        LEXICON["profile_ask_experience"],
        reply_markup=get_experience_keyboard()
    )
    await state.set_state(ProfileStates.experience)


# ============================================
# ШАГ 2: ОПЫТ
# ============================================
@profile_router.callback_query(StateFilter(ProfileStates.experience), F.data.in_([
    "exp_0_1", "exp_1_3", "exp_3plus"
]))
async def process_experience(callback: CallbackQuery, state: FSMContext):
    exp_map = {
        "exp_0_1": LEXICON["exp_0_1"],
        "exp_1_3": LEXICON["exp_1_3"],
        "exp_3plus": LEXICON["exp_3plus"]
    }

    experience = exp_map.get(callback.data, "не указано")
    await state.update_data(experience=experience)

    await callback.message.delete()
    await callback.message.answer(LEXICON["profile_ask_goals"])
    await state.set_state(ProfileStates.goals)
    await callback.answer()


# ============================================
# ШАГ 3: ЦЕЛИ
# ============================================
@profile_router.message(StateFilter(ProfileStates.goals))
async def process_goals(message: Message, state: FSMContext):
    goals_text = message.text.strip()

    if len(goals_text) < 3:
        await message.answer("❌ Слишком коротко. Опишите ваши цели подробнее:")
        return

    await state.update_data(goals=goals_text)

    # Показываем данные для подтверждения
    data = await state.get_data()

    text = LEXICON["profile_confirm"].format(
        stack=data['stack'],
        experience=data['experience'],
        goals=data['goals']
    )

    await message.answer(
        text,
        parse_mode='HTML',
        reply_markup=get_profile_confirm_keyboard()
    )
    await state.set_state(ProfileStates.confirm)


# ============================================
# ПОДТВЕРЖДЕНИЕ: СОХРАНИТЬ
# ============================================
@profile_router.callback_query(StateFilter(ProfileStates.confirm), F.data == "profile_save")
async def process_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    success = db_service.save_user_profile(
        user_id=user_id,
        stack=data['stack'],
        experience=data['experience'],
        goals=data['goals']
    )

    await callback.message.delete()

    if success:
        await callback.message.answer(LEXICON["profile_saved"])
    else:
        await callback.message.answer(LEXICON["profile_save_error"])

    await state.clear()
    await callback.answer()


# ============================================
# ПОДТВЕРЖДЕНИЕ: ЗАПОЛНИТЬ ЗАНОВО
# ============================================
@profile_router.callback_query(StateFilter(ProfileStates.confirm), F.data == "profile_restart")
async def process_restart(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LEXICON["profile_ask_stack"])
    await state.set_state(ProfileStates.stack)
    await callback.answer()


# ============================================
# ОБРАБОТКА НЕКОРРЕКТНОГО ВВОДА
# ============================================
@profile_router.message(StateFilter(ProfileStates.experience))
async def warning_not_experience(message: Message):
    await message.answer(LEXICON["warning_not_experience"])


@profile_router.message(StateFilter(ProfileStates.confirm))
async def warning_not_confirm(message: Message):
    await message.answer(LEXICON["warning_not_confirm"])