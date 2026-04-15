"""Парсер Kwork.ru (с использованием Selenium)"""
import sys
import os
import re
from concurrent.futures import ThreadPoolExecutor
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.db import insert_into_db

# Пути для NIXOS
CHROME_PATH = "/nix/store/s1az0if85pclia1vdlh0a3hf93wah342-chromium-144.0.7559.132/bin/chromium"
DRIVER_PATH = "/home/oleg/.nix-profile/bin/chromedriver"

def clean_price(price_text: str) -> str:
    """Очистка цены от мусора"""
    if not price_text:
        return "Цена не указана"

    numbers = re.findall(r'(\d[\d\s]*\d|\d)', price_text)
    if numbers:
        price = re.sub(r'\s', '', numbers[0])
        return f"{price} ₽"
    return "Цена не указана"

def parse_page_sync(page: int) -> list:
    """Синхронный парсинг одной страницы Kwork"""
    chrome_options = Options()
    chrome_options.binary_location = CHROME_PATH
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    projects = []

    try:
        url = f"https://kwork.ru/projects?a=1&page={page}"
        print(f"📄 [Kwork] Загрузка страницы {page}")

        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wants-content"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.find_all('div', class_='wants-card__top')

        for card in cards:
            try:
                left_part = card.find('div', class_='wants-card__left')
                title_link = left_part.find('h1', class_='wants-card__header-title').find('a')

                title = title_link.text.strip() if title_link else "Без названия"
                href = title_link.get('href', '') if title_link else ''
                project_id = href.replace('/projects/', '') if href else ''
                link = f"https://kwork.ru/projects/{project_id}/view" if project_id else ""

                desc_elem = left_part.find('div', class_='wants-card__description-text')
                description = desc_elem.text.strip() if desc_elem else ""

                price_elem = card.find('div', class_='wants-card__right')
                price = clean_price(price_elem.text.strip() if price_elem else "")

                insert_into_db(title, price, description, link, project_id, source='kwork')

                projects.append({
                    "title": title, "price": price, "description": description,
                    "link": link, "project_id": project_id, "source": "kwork"
                })
                print(f"✅ [Kwork] {title[:40]}... | {price}")

            except Exception as e:
                print(f"⚠️ [Kwork] Ошибка: {e}")
                continue

    finally:
        driver.quit()

    return projects

class KworkParser:
    """Парсер Kwork"""

    def __init__(self):
        self.source = "kwork"

    async def run(self, pages: int = 2) -> list:
        """Асинхронный запуск парсера Kwork"""
        print(f"\n🚀 Запуск парсера Kwork ({pages} страниц)")

        with ThreadPoolExecutor(max_workers=3) as executor:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(executor, parse_page_sync, page)
                    for page in range(1, pages + 1)]
            results = await asyncio.gather(*tasks)

        all_projects = []
        for projects in results:
            all_projects.extend(projects)

        print(f"✅ [Kwork] Собрано {len(all_projects)} проектов")
        return all_projects