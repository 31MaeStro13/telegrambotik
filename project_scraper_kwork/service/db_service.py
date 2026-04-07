import logging
from db.db import connect_db
from vector_db.chroma_client import get_projects_collection

# Получаем логгер для этого модуля
logger = logging.getLogger(__name__)


# ============================================
# Функция 1: Добавить в избранное
# ============================================
def add_to_favorites(
    user_id: int,
    project_id: str,
    name: str,
    price: str,
    description: str,
    link: str
) -> bool:
    """
    Добавляет проект в избранное пользователя
    Возвращает True, если добавлено, False если уже было или ошибка
    """
    # Логируем попытку (уровень DEBUG — для отладки)
    logger.debug(f"Попытка добавить в избранное: user_id={user_id}, project_id={project_id}")

    # Подключаемся к БД
    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return False

    try:
        # Создаём курсор — это объект для выполнения запросов
        cursor = conn.cursor()

        # Выполняем SQL-запрос
        # INSERT IGNORE — если такая запись уже есть, просто проигнорировать
        cursor.execute('''
            INSERT IGNORE INTO favorites (user_id, project_id, name, price, description, link)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user_id, project_id, name, price, description, link))

        # Подтверждаем изменения в БД
        conn.commit()

        # cursor.rowcount — сколько строк реально добавилось
        if cursor.rowcount > 0:
            logger.info(f"✅ Проект {project_id} добавлен в избранное пользователя {user_id}")
            return True
        else:
            logger.info(f"⏭️ Проект {project_id} уже был в избранном у пользователя {user_id}")
            return False

    except Exception as e:
        # Логируем ошибку с полным стеком (exc_info=True)
        logger.error(f"Ошибка добавления в избранное: {e}", exc_info=True)
        return False

    finally:
        # Закрываем курсор и соединение (чтобы не было утечек)
        try:
            cursor.close()
            conn.close()
        except:
            pass


# ============================================
# Функция 2: Удалить из избранного
# ============================================
def remove_from_favorites(user_id: int, project_id: str) -> bool:
    """
    Удаляет проект из избранного пользователя
    Возвращает True, если удалено, False если не было или ошибка
    """
    logger.debug(f"Попытка удалить из избранного: user_id={user_id}, project_id={project_id}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM favorites WHERE user_id = %s AND project_id = %s
        ''', (user_id, project_id))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"🗑 Проект {project_id} удалён из избранного пользователя {user_id}")
            return True
        else:
            logger.info(f"⏭️ Проект {project_id} не был в избранном у пользователя {user_id}")
            return False

    except Exception as e:
        logger.error(f"Ошибка удаления из избранного: {e}", exc_info=True)
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# ============================================
# Функция 3: Получить избранное пользователя
# ============================================
def get_user_favorites(user_id: int, limit: int = 10) -> list:
    """
    Получает список избранных проектов пользователя
    Возвращает список словарей
    """
    logger.debug(f"Запрос избранного для user_id={user_id}, limit={limit}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return []

    projects = []
    try:
        # dictionary=True — чтобы результаты приходили в виде словарей
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT project_id, name, price, description, link
            FROM favorites
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        ''', (user_id, limit))

        # fetchall() — получить все строки
        for row in cursor.fetchall():
            projects.append({
                'project_id': row['project_id'],
                'name': row['name'],
                'price': row['price'],
                'description': row['description'],
                'link': row['link']
            })

        logger.info(f"📦 Найдено {len(projects)} избранных проектов для user_id={user_id}")
        return projects

    except Exception as e:
        logger.error(f"Ошибка получения избранного: {e}", exc_info=True)
        return []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# ============================================
# Функция 4: Добавить в скрытые
# ============================================
def add_to_hidden(user_id: int, project_id: str) -> bool:
    """
    Добавляет проект в скрытые пользователя
    """
    logger.debug(f"Попытка скрыть проект: user_id={user_id}, project_id={project_id}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT IGNORE INTO hidden (user_id, project_id)
            VALUES (%s, %s)
        ''', (user_id, project_id))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"🙈 Проект {project_id} скрыт для пользователя {user_id}")
            return True
        else:
            logger.info(f"⏭️ Проект {project_id} уже был скрыт у пользователя {user_id}")
            return False

    except Exception as e:
        logger.error(f"Ошибка добавления в скрытые: {e}", exc_info=True)
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# ============================================
# Функция 5: Получить проект по ID
# ============================================
def get_project_by_id(project_id: str) -> dict | None:
    """
    Получает полные данные проекта из основной таблицы
    Возвращает словарь или None, если проект не найден
    """
    logger.debug(f"Запрос проекта по ID: {project_id}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT name, price, description, link
            FROM kwork_projects
            WHERE project_id = %s
        ''', (project_id,))

        project = cursor.fetchone()

        if project:
            logger.debug(f"✅ Проект {project_id} найден")
            return project
        else:
            logger.warning(f"⚠️ Проект {project_id} не найден в БД")
            return None

    except Exception as e:
        logger.error(f"Ошибка получения проекта: {e}", exc_info=True)
        return None
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def get_hidden_projects(user_id: int) -> list:
    """
    Возвращает список project_id, которые пользователь скрыл
    """
    logger.debug(f"Запрос скрытых проектов для user_id={user_id}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return []

    projects = []
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT project_id FROM hidden WHERE user_id = %s
        ''', (user_id,))

        for row in cursor.fetchall():
            projects.append(row[0])

        logger.info(f"📦 Найдено {len(projects)} скрытых проектов для user_id={user_id}")
        return projects

    except Exception as e:
        logger.error(f"Ошибка получения скрытых проектов: {e}", exc_info=True)
        return []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def remove_from_hidden(user_id: int, project_id: str) -> bool:
    """Убирает проект из скрытых (восстанавливает)"""
    logger.debug(f"Попытка восстановить проект: user_id={user_id}, project_id={project_id}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM hidden WHERE user_id = %s AND project_id = %s
        ''', (user_id, project_id))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"🔄 Проект {project_id} восстановлен для пользователя {user_id}")
            return True
        else:
            logger.info(f"⏭️ Проект {project_id} не был в скрытых у пользователя {user_id}")
            return False

    except Exception as e:
        logger.error(f"Ошибка восстановления проекта: {e}", exc_info=True)
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass



def get_visible_projects(user_id: int, limit: int = 10) -> list:
    """
    Получает проекты из kwork_projects, исключая те,
    которые пользователь скрыл (есть в таблице hidden)
    """
    logger.debug(f"Запрос видимых проектов для user_id={user_id}, limit={limit}")

    conn = connect_db()
    if not conn:
        logger.error("Не удалось подключиться к БД")
        return []

    projects = []
    try:
        cursor = conn.cursor(dictionary=True)

        # LEFT JOIN + WHERE hidden.project_id IS NULL — берём только те, которых нет в hidden
        cursor.execute('''
            SELECT p.project_id, p.name, p.price, p.description, p.link
            FROM kwork_projects p
            LEFT JOIN hidden h ON p.project_id = h.project_id AND h.user_id = %s
            WHERE h.project_id IS NULL
            ORDER BY p.created_at DESC
            LIMIT %s
        ''', (user_id, limit))

        for row in cursor.fetchall():
            projects.append({
                'project_id': row['project_id'],
                'name': row['name'],
                'price': row['price'],
                'description': row['description'],
                'link': row['link']
            })

        logger.info(f"📦 Найдено {len(projects)} видимых проектов для user_id={user_id}")
        return projects

    except Exception as e:
        logger.error(f"Ошибка получения видимых проектов: {e}", exc_info=True)
        return []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def get_total_projects_count() -> int:
    """Общее количество проектов в БД"""
    conn = connect_db()
    if not conn:
        return 0

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM kwork_projects')
        return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Ошибка получения общего количества: {e}")
        return 0
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def get_today_projects_count() -> int:
    """Количество проектов, добавленных сегодня"""
    conn = connect_db()
    if not conn:
        return 0

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM kwork_projects
            WHERE DATE(created_at) = CURDATE()
        ''')
        return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Ошибка получения сегодняшних проектов: {e}")
        return 0
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def get_last_update_time() -> str:
    """Время последнего добавленного проекта"""
    conn = connect_db()
    if not conn:
        return "неизвестно"

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT created_at FROM kwork_projects
            ORDER BY created_at DESC
            LIMIT 1
        ''')
        result = cursor.fetchone()
        if result:
            return result[0].strftime("%d.%m.%Y %H:%M")
        return "нет данных"
    except Exception as e:
        logger.error(f"Ошибка получения времени последнего обновления: {e}")
        return "ошибка"
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass



def save_user_profile(user_id: int, stack: str, experience: str, goals: str) -> bool:
    """Сохраняет или обновляет профиль пользователя"""
    logger.debug(f"Сохранение профиля для user_id={user_id}")

    conn = connect_db()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_profiles (user_id, stack, experience, goals)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                stack = VALUES(stack),
                experience = VALUES(experience),
                goals = VALUES(goals),
                updated_at = CURRENT_TIMESTAMP
        ''', (user_id, stack, experience, goals))
        conn.commit()

        logger.info(f"✅ Профиль сохранён для user_id={user_id}")
        return True

    except Exception as e:
        logger.error(f"Ошибка сохранения профиля: {e}", exc_info=True)
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def get_user_profile(user_id: int) -> dict | None:
    """Получает профиль пользователя"""
    logger.debug(f"Запрос профиля для user_id={user_id}")

    conn = connect_db()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT stack, experience, goals, created_at, updated_at
            FROM user_profiles
            WHERE user_id = %s
        ''', (user_id,))

        return cursor.fetchone()

    except Exception as e:
        logger.error(f"Ошибка получения профиля: {e}", exc_info=True)
        return None
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass



def add_project_to_vector_db(project_id: str, title: str, description: str) -> bool:
    """
    Добавляет проект в векторную БД
    """
    logger.debug(f"Добавление проекта {project_id} в векторную БД")

    try:
        collection = get_projects_collection()

        # Объединяем название и описание для поиска
        text_for_search = f"{title}\n{description}"

        collection.add(
            documents=[text_for_search],
            metadatas=[{"project_id": project_id, "title": title}],
            ids=[project_id]
        )

        logger.info(f"✅ Проект {project_id} добавлен в векторную БД")
        return True

    except Exception as e:
        logger.error(f"Ошибка добавления проекта в векторную БД: {e}")
        return False


def get_new_projects_for_vector(vector_ids: list) -> list:
    """
    Возвращает проекты из MySQL, которых ещё нет в векторной БД
    """
    conn = connect_db()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        # Если список пустой — берём все
        if not vector_ids:
            cursor.execute('''
                SELECT project_id, name, description FROM kwork_projects
            ''')
        else:
            # Создаём плейсхолдеры для SQL
            placeholders = ','.join(['%s'] * len(vector_ids))
            cursor.execute(f'''
                SELECT project_id, name, description FROM kwork_projects
                WHERE project_id NOT IN ({placeholders})
            ''', vector_ids)

        return cursor.fetchall()

    except Exception as e:
        logger.error(f"Ошибка получения новых проектов: {e}")
        return []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass