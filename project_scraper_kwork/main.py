import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis

from config.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
from handlers.profile import profile_router
from keyboard.menu_commands import set_main_menu
from migrations.sync_vector_db import periodic_vector_sync

from handlers.callbacks.favorites import fav_router
from handlers.callbacks.hidden import hidden_router
from handlers.callbacks.profile import profile_callback_router
from handlers.callbacks.more import more_router
from handlers.recommend import recommend_router

from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp

logger = logging.getLogger(__name__)


async def main():

    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(config.log.level),
        format=config.log.format,
    )

    # Создаём Redis клиент
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0
    )

    # Создаём хранилище для FSM
    storage = RedisStorage(redis_client)



    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)


    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(profile_router)
    dp.include_router(fav_router)
    dp.include_router(hidden_router)
    dp.include_router(profile_callback_router)
    dp.include_router(more_router)
    dp.include_router(recommend_router)
    dp.include_router(other_router)

    # функция для перевода данных в векторную бд раз в час
    asyncio.create_task(periodic_vector_sync(interval_seconds=3600))

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())