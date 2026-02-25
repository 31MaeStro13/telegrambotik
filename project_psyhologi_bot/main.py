import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers.dialog import router_dialog
from handlers.command import router_command
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)

async def main():

    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.formatlog,
    )

    logger.info("Starting bot")

    bot = Bot (
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(router_command)
    dp.include_router(router_dialog)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())