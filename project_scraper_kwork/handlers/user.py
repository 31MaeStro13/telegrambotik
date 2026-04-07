from aiogram import F, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from handlers.profile import ProfileStates
from db.db import get_recent_projects
from lexicon.lexicon import LEXICON
from keyboard.favorit_kb import create_inline_favorit_kb, get_favorite_keyboard, get_hidden_keyboard
from keyboard.profile_kb import get_profile_edit_keyboard

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'service'))
from service.service import clean_price, truncate_description
import service.db_service as db_service

user_router = Router()

# Хранилища для последних сообщений
last_favorites_message = {}  # {user_id: message_id}
last_hidden_message = {}     # {user_id: message_id}


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start_text'])


@user_router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help_text'])


@user_router.message(Command('favorites'))
async def process_favorites(message: Message):
    user_id = message.from_user.id
    favorites = db_service.get_user_favorites(user_id, limit=10)

    # Удаляем предыдущее сообщение, если было
    if user_id in last_favorites_message:
        try:
            await message.bot.delete_message(
                chat_id=user_id,
                message_id=last_favorites_message[user_id]
            )
        except:
            pass

    if not favorites:
        sent = await message.answer(LEXICON["no_favorites"])
        last_favorites_message[user_id] = sent.message_id
        return

    for i, project in enumerate(favorites, 1):
        clean_price_text = clean_price(project['price'])

        text = LEXICON["favorite_template"].format(
            number=i,
            name=project['name'],
            price=clean_price_text,
            description=truncate_description(project['description'], 100)
        )

        keyboard = get_favorite_keyboard(project['project_id'])

        sent = await message.answer(
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        # Сохраняем ID последнего сообщения
        last_favorites_message[user_id] = sent.message_id


@user_router.message(Command('hidden'))
async def process_hidden(message: Message):
    user_id = message.from_user.id
    hidden_ids = db_service.get_hidden_projects(user_id)

    # Удаляем предыдущее сообщение, если было
    if user_id in last_hidden_message:
        try:
            await message.bot.delete_message(
                chat_id=user_id,
                message_id=last_hidden_message[user_id]
            )
        except:
            pass

    if not hidden_ids:
        sent = await message.answer(LEXICON["no_hidden"])
        last_hidden_message[user_id] = sent.message_id
        return

    for i, project_id in enumerate(hidden_ids, 1):
        project = db_service.get_project_by_id(project_id)
        if not project:
            continue

        clean_price_text = clean_price(project['price'])

        text = LEXICON["hidden_template"].format(
            number=i,
            name=project['name'],
            price=clean_price_text,
            description=truncate_description(project['description'], 100)
        )

        keyboard = get_hidden_keyboard(project_id)

        sent = await message.answer(
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        # Сохраняем ID последнего сообщения
        last_hidden_message[user_id] = sent.message_id


@user_router.message(Command('data'))
async def show_data_command(message: Message):
    try:
        user_id = message.from_user.id
        projects = db_service.get_visible_projects(user_id, limit=10)

        if not projects:
            await message.answer(LEXICON["no_data"])
            return

        for i, project in enumerate(projects, 1):
            clean_price_text = clean_price(project['price'])
            short_desc = truncate_description(project['description'], 200)
            has_more = len(project['description']) > 200

            text = LEXICON["data_project_template"].format(
                number=i,
                name=project['name'],
                price=clean_price_text,
                description=short_desc,
                link=project['link']
            )

            keyboard = create_inline_favorit_kb(
                project_id=project['project_id'],
                has_more=has_more
            )

            await message.answer(
                text=text,
                parse_mode='Markdown',
                reply_markup=keyboard
            )

    except Exception as e:
        await message.answer(LEXICON["error_data"])


@user_router.message(Command('stats'))
async def show_stats(message: Message):
    try:
        total = db_service.get_total_projects_count()
        today = db_service.get_today_projects_count()
        last_update = db_service.get_last_update_time()

        text = LEXICON["stats"].format(
            total=total,
            today=today,
            last_update=last_update
        )

        await message.answer(text, parse_mode='HTML')

    except Exception as e:
        await message.answer(LEXICON["error_data"])


@user_router.message(Command('profile'))
async def process_profile_command(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверяем, есть ли профиль в БД
    profile = db_service.get_user_profile(user_id)

    if profile:
        # Профиль есть — показываем
        text = LEXICON["profile_view"].format(
            stack=profile['stack'],
            experience=profile['experience'],
            goals=profile['goals'],
            created=profile['created_at'].strftime("%d.%m.%Y") if profile['created_at'] else "неизвестно",
            updated=profile['updated_at'].strftime("%d.%m.%Y %H:%M") if profile['updated_at'] else "неизвестно"
        )



        await message.answer(
            text=text,
            parse_mode='HTML',
            reply_markup=get_profile_edit_keyboard()
        )
    else:
        # Профиля нет — предлагаем создать
        await message.answer(LEXICON["profile_start"])


@user_router.message(Command('edit_profile'))
async def process_edit_profile_command(message: Message, state: FSMContext):
    # Запускаем FSM сначала
    await state.clear()
    await message.answer(LEXICON["profile_ask_stack"])
    await state.set_state(ProfileStates.stack)


@user_router.message(Command('cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(LEXICON["cancel"])


@user_router.message(Command('cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(LEXICON["profile_cancel"])
    await state.clear()
