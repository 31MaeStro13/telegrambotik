import logging
import asyncio

from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import other, user


async def main() -> None:

    config: Config = load_config()

    print(f"Config: {config}")
    print(f"Bot token exists: {hasattr(config.bot, 'token')}")
    print(f"Log exists: {hasattr(config, 'log')}")

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )

    bot = Bot(config.bot.token)
    dp = Dispatcher()

    dp.include_router(user.router)
    dp.include_router(other.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
