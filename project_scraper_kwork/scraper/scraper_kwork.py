import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Добавляем путь к папке db
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.db import insert_into_db, export_to_excel

# ============================================
# ПУТИ ДЛЯ NIXOS
# ============================================
chrome_path = "/nix/store/s1az0if85pclia1vdlh0a3hf93wah342-chromium-144.0.7559.132/bin/chromium"
driver_path = "/home/oleg/.nix-profile/bin/chromedriver"

print(f"✅ Браузер: {chrome_path}")
print(f"✅ Драйвер: {driver_path}")

# ============================================
# НАСТРОЙКИ БРАУЗЕРА
# ============================================
chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# ============================================
# ФУНКЦИИ ПАРСИНГА
# ============================================
def parse_with_bs(html):
    """Парсит HTML с помощью BeautifulSoup и сохраняет в БД"""
    soup = BeautifulSoup(html, 'html.parser')
    projects = []

    wants_content = soup.find('div', class_='wants-content')
    if not wants_content:
        print("❌ Не найден wants-content")
        return projects

    cards = wants_content.find_all('div', class_='wants-card__top')
    print(f"🔍 Найдено карточек: {len(cards)}")

    for card in cards:
        try:
            # Название и ссылка
            left_part = card.find('div', class_='wants-card__left')
            title_h1 = left_part.find('h1', class_='wants-card__header-title')
            title_link = title_h1.find('a')

            title = title_link.text.strip() if title_link else "Без названия"

            # Извлекаем ID проекта из атрибута href
            href = title_link.get('href', '') if title_link else ''
            project_id = href.replace('/projects/', '') if href else ''

            # Формируем полную ссылку
            full_link = f"https://kwork.ru/projects/{project_id}/view" if project_id else ""

            # Описание
            desc_elem = left_part.find('div', class_='wants-card__description-text')
            description = desc_elem.text.strip() if desc_elem else ""

            # Цена
            price_elem = card.find('div', class_='wants-card__right')
            price = price_elem.text.strip() if price_elem else "Цена не указана"

            # Сохраняем в БД
            insert_into_db(title, price, description, full_link, project_id)

            projects.append({
                "title": title,
                "price": price,
                "description": description,
                "link": full_link,
                "project_id": project_id
            })

            print(f"✅ {title[:30]}... | {price[:20]}... | ID: {project_id}")

        except Exception as e:
            print(f"⚠️ Ошибка парсинга карточки: {e}")
            continue

    return projects

def parse_kwork(pages=2):
    """Основная функция парсинга"""
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    all_projects = []

    try:
        for page in range(1, pages + 1):
            url = f"https://kwork.ru/projects?a=1&page={page}"
            print(f"\n📄 Страница {page}")

            driver.get(url)
            time.sleep(5)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "wants-content"))
                )
            except TimeoutException:
                print("❌ Таймаут загрузки")
                continue

            html = driver.page_source
            projects = parse_with_bs(html)
            all_projects.extend(projects)

            time.sleep(2)

    finally:
        driver.quit()

    return all_projects

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    projects = parse_kwork(pages=2)

    print("\n" + "="*50)
    print(f"📦 ВСЕГО ПРОЕКТОВ: {len(projects)}")
    print("="*50)

    # Экспортируем в Excel
    export_to_excel()
    print(f"\n✅ Данные сохранены в БД и экспортированы в Excel")