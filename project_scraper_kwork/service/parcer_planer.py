"""Планировщик задач для парсеров"""
import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scraper.kwork import KworkParser
from scraper.fl import FlParser
from scraper.weblancer import WeblancerParser
from scraper.freelance_ru import FreelanceRuParser
from db.db import export_to_excel

logger = logging.getLogger(__name__)

# Создаем глобальный планировщик
scheduler = AsyncIOScheduler()


async def run_all_parsers():
    """Запуск всех парсеров"""
    logger.info("🔄 Запуск планового парсинга...")
    start_time = datetime.now()

    try:
        # Создаем экземпляры парсеров
        kwork = KworkParser()
        fl = FlParser()
        weblancer = WeblancerParser()
        freelance_ru = FreelanceRuParser()

        # Запускаем все парсеры параллельно
        results = await asyncio.gather(
            kwork.run(pages=2),
            fl.run(pages=2),
            weblancer.run(pages=2),
            freelance_ru.run(pages=2),
            return_exceptions=True
        )

        kwork_projects, fl_projects, weblancer_projects, freelance_ru_projects = results

        # Считаем успешные результаты
        kwork_count = len(kwork_projects) if isinstance(kwork_projects, list) else 0
        fl_count = len(fl_projects) if isinstance(fl_projects, list) else 0
        weblancer_count = len(weblancer_projects) if isinstance(weblancer_projects, list) else 0

        total = kwork_count + fl_count + weblancer_count

        # Экспортируем в Excel
        export_to_excel()

        elapsed = (datetime.now() - start_time).total_seconds()

        logger.info(f"✅ Парсинг завершен за {elapsed:.2f} сек")
        logger.info(f"📊 Результаты: Kwork={kwork_count}, FL.ru={fl_count}, Weblancer={weblancer_count}, Всего={total}")

        return {
            "success": True,
            "kwork": kwork_count,
            "fl": fl_count,
            "weblancer": weblancer_count,
            "total": total,
            "time": elapsed
        }

    except Exception as e:
        logger.error(f"❌ Ошибка при парсинге: {e}")
        return {"success": False, "error": str(e)}


def start_scheduler():
    """Запуск планировщика"""
    # Добавляем задачу: запускать каждый час
    scheduler.add_job(
        run_all_parsers,
        trigger=IntervalTrigger(hours=1),
        id="hourly_parsing",
        replace_existing=True
    )

    # Запускаем планировщик
    scheduler.start()
    logger.info("⏰ Планировщик запущен. Парсинг будет выполняться каждый час")


def stop_scheduler():
    """Остановка планировщика"""
    scheduler.shutdown()
    logger.info("⏰ Планировщик остановлен")