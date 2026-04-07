#!/usr/bin/env python
import sys
import os
import asyncio
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from service.db_service import add_project_to_vector_db, get_new_projects_for_vector
from vector_db.chroma_client import get_all_vector_ids

logger = logging.getLogger(__name__)

# ============================================
# ОСНОВНАЯ ЛОГИКА СИНХРОНИЗАЦИИ
# ============================================
def _sync_vector_db():
    """Добавляет в векторную БД только новые проекты из MySQL"""
    logger.info("🔄 Запуск синхронизации с векторной БД")

    vector_ids = get_all_vector_ids()
    logger.info(f"📦 В векторной БД: {len(vector_ids)} проектов")

    new_projects = get_new_projects_for_vector(vector_ids)
    logger.info(f"🆕 Новых проектов для добавления: {len(new_projects)}")

    if not new_projects:
        logger.info("✅ Всё уже синхронизировано")
        return

    success_count = 0
    for project in new_projects:
        if add_project_to_vector_db(
            project_id=project['project_id'],
            title=project['name'],
            description=project['description']
        ):
            success_count += 1

    logger.info(f"✅ Добавлено {success_count} из {len(new_projects)} новых проектов")


# ============================================
# ОБЁРТКА ДЛЯ ПЕРИОДИЧЕСКОГО ЗАПУСКА
# ============================================
async def periodic_vector_sync(interval_seconds: int = 3600):
    """Фоновая задача: запускает sync_vector_db() каждые interval_seconds секунд"""
    while True:
        try:
            await asyncio.to_thread(_sync_vector_db)
            logger.info(f"⏳ Следующая синхронизация через {interval_seconds // 60} минут")
        except Exception as e:
            logger.error(f"❌ Ошибка в periodic_vector_sync: {e}")

        await asyncio.sleep(interval_seconds)


# ============================================
# ТОЧКА ВХОДА ДЛЯ РУЧНОГО ЗАПУСКА
# ============================================
if __name__ == "__main__":
    _sync_vector_db()