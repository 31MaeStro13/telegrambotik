from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from service.db_service import get_user_profile
from ai_agent.ai_agent import recommendation_agent

recommend_router = Router()

@recommend_router.message(Command("recommend"))
async def handle_recommend(message: Message):
    user_id = message.from_user.id
    profile = get_user_profile(user_id)

    if not profile:
        await message.answer("❌ Сначала создайте профиль через /profile")
        return

    # Формируем запрос для агента
    prompt = (
        f"Пользователь имеет следующий профиль:\n"
        f"Стек: {profile['stack']}\n"
        f"Опыт: {profile['experience']}\n"
        f"Цели: {profile['goals']}\n\n"
        f"Найди в базе знаний подходящие проекты и объясни, почему они подходят."
    )

    await message.answer("🔍 Анализирую профиль и ищу проекты...")

    response = await recommendation_agent.run(prompt)
    await message.answer(response.content)