import mysql.connector
import pandas as pd

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
from config.config import Config, load_config

config: Config = load_config()

# Конфигурация подключения
DB_CONFIG = {
    'user': config.data.user,
    'password': config.data.password,
    'host': config.data.host,
    'database': config.data.database,
    'port': config.data.port
}

# Функция подключения к базе данных и создания таблицы
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        create_table_if_not_exists(conn)
        return conn
    except mysql.connector.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

# Создание таблицы, если не существует
def create_table_if_not_exists(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kwork_projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT NOT NULL,
                price TEXT,
                description TEXT,
                link TEXT,
                project_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        try:
            cursor.close()
        except:
            pass

# Проверка на дубликат перед вставкой (учитываем project_id)
def check_if_exists(conn, project_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM kwork_projects WHERE project_id = %s
        ''', (project_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except mysql.connector.Error as e:
        print(f"Ошибка при проверке дубликатов: {e}")
        return False
    finally:
        try:
            cursor.close()
        except:
            pass

# Вставка данных с проверкой на дубликаты
def insert_into_db(name, price, description, link, project_id, source='kwork', external_id=None):
    conn = connect_db()
    if not conn:
        return False

    try:
        if check_if_exists(conn, project_id):
            print(f"⏭️ Дубликат: {project_id} уже есть в БД")
            return False

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO kwork_projects (name, price, description, link, project_id, source, external_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (name, price, description, link, project_id, source, external_id))
        conn.commit()
        print(f"✅ Добавлен: {name[:30]}...")
        return True
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# Экспорт данных из базы в Excel
def export_to_excel():
    try:
        conn = connect_db()
        if conn:
            query = "SELECT id, name, price, description, link, project_id, created_at FROM kwork_projects"
            df = pd.read_sql(query, conn)
            df.to_excel("kwork_projects.xlsx", index=False, engine='openpyxl')
            print("Данные успешно экспортированы в kwork_projects.xlsx")
            conn.close()
    except Exception as e:
        print(f"Ошибка при экспорте данных в Excel: {e}")

def get_recent_projects(limit=10):
    """Получает последние проекты из БД"""
    conn = connect_db()
    if not conn:
        return []

    projects = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT name, price, description, link, project_id, created_at
            FROM kwork_projects
            ORDER BY created_at DESC
            LIMIT %s
        ''', (limit,))

        for row in cursor.fetchall():
            projects.append({
                'name': row['name'],
                'price': row['price'],
                'description': row['description'],
                'link': row['link'],
                'project_id': row['project_id'],
                'created_at': row['created_at']
            })
    except Exception as e:
        print(f"Ошибка при получении проектов: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    return projects

# Пример использования
if __name__ == "__main__":
    # Пример вставки (замените на реальные переменные из вашего парсера)
    # insert_into_db(title, price, description, link, project_id)

    # Экспорт данных в Excel
    export_to_excel()