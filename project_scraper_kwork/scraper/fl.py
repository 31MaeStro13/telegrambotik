"""Парсер FL.ru"""
import sys
import os
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.db import insert_into_db
from .base_parser import BaseParser

class FlParser(BaseParser):
    """Парсер FL.ru"""

    def __init__(self):
        super().__init__('fl')
        self.base_url = 'https://www.fl.ru/projects/?kind=1'

    def clean_price(self, price_text: str) -> str:
        """Очистка цены"""
        if not price_text:
            return "Цена не указана"

        if 'по договоренности' in price_text.lower():
            return "По договоренности"

        numbers = re.findall(r'(\d[\d\s]*\d|\d)', price_text)
        if numbers:
            price = re.sub(r'\s', '', numbers[0])
            return f"{price} ₽"

        return price_text

    def parse_projects(self, html: str, page: int) -> List[Dict]:
        """Парсинг страницы"""
        soup = BeautifulSoup(html, 'html.parser')
        projects = []

        cards = soup.find_all('div', class_='b-page__lenta_item')

        for card in cards:
            try:
                title_elem = card.find('h2', class_='b-post__title')
                if not title_elem:
                    continue

                link_elem = title_elem.find('a')
                if not link_elem:
                    continue

                title = link_elem.text.strip()
                href = link_elem.get('href', '')
                link = f"https://www.fl.ru{href}" if href else ""

                project_id = None
                if href:
                    match = re.search(r'/projects/(\d+)/', href)
                    if match:
                        project_id = match.group(1)

                price_elem = card.find('div', class_='b-post__price')
                price = "Цена не указана"
                if price_elem:
                    price_span = price_elem.find('span', class_='text-4')
                    if price_span:
                        price = self.clean_price(price_span.text.strip())

                desc_elem = card.find('div', class_='b-post__body')
                description = ""
                if desc_elem:
                    desc_text = desc_elem.find('div', class_='b-post__txt')
                    if desc_text:
                        description = desc_text.text.strip()

                if not project_id:
                    continue

                insert_into_db(title, price, description, link, project_id, source=self.source)

                projects.append({
                    "title": title, "price": price, "description": description,
                    "link": link, "project_id": project_id, "source": self.source
                })
                print(f"✅ [FL.ru] {title[:50]}... | {price}")

            except Exception as e:
                print(f"⚠️ [FL.ru] Ошибка: {e}")
                continue

        print(f"📊 [FL.ru] Страница {page}: найдено {len(projects)} проектов")
        return projects

    async def run(self, pages: int = 2) -> List[Dict]:
        """Запуск парсера"""
        print(f"\n🚀 Запуск парсера FL.ru ({pages} страниц)")
        all_projects = []

        async with aiohttp.ClientSession() as session:
            for page in range(1, pages + 1):
                if page == 1:
                    url = self.base_url
                else:
                    url = f"https://www.fl.ru/projects/page-{page}/?kind=1"

                html = await self.fetch(session, url)
                if html:
                    projects = self.parse_projects(html, page)
                    all_projects.extend(projects)
                await asyncio.sleep(0.5)

        print(f"✅ [FL.ru] Собрано {len(all_projects)} проектов")
        return all_projects