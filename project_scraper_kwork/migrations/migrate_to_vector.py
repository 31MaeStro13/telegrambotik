import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from service.db_service import add_project_to_vector_db
from db.db import connect_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_all_projects():
    """Переносит все проекты из MySQL в векторную БД"""

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT project_id, name, description FROM kwork_projects
        ''')

        projects = cursor.fetchall()
        logger.info(f"Найдено {len(projects)} проектов для миграции")

        success_count = 0
        for project in projects:
            if add_project_to_vector_db(
                project_id=project['project_id'],
                title=project['name'],
                description=project['description']
            ):
                success_count += 1

        logger.info(f"✅ Успешно перенесено {success_count} из {len(projects)} проектов")

    except Exception as e:
        logger.error(f"Ошибка при миграции: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    migrate_all_projects()