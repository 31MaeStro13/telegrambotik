"""Парсер Weblancer.net"""
import sys
import os
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.db import insert_into_db

class WeblancerParser:
    """Парсер Weblancer"""

    def __init__(self):
        self.source = "weblancer"
        self.base_url = "https://www.weblancer.net/freelance/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }

    async def fetch(self, session: aiohttp.ClientSession, url: str, retry: int = 3):
        """Асинхронный GET запрос"""
        for attempt in range(retry):
            try:
                async with session.get(url, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"⚠️ [Weblancer] Статус {response.status}, попытка {attempt + 1}")
            except Exception as e:
                print(f"❌ [Weblancer] Ошибка: {e}, попытка {attempt + 1}")

            if attempt < retry - 1:
                await asyncio.sleep(2 ** attempt)
        return None

    def parse_projects(self, html: str, page: int) -> List[Dict]:
        """Парсинг страницы Weblancer"""
        soup = BeautifulSoup(html, 'html.parser')
        projects = []

        # Карточки проектов
        cards = soup.find_all('article', class_='bg-white')

        for card in cards:
            try:
                # Название и ссылка
                title_elem = card.find('h2', class_='text-xl')
                if not title_elem:
                    continue

                link_elem = title_elem.find('a')
                if not link_elem:
                    continue

                title = link_elem.text.strip()
                href = link_elem.get('href', '')
                link = f"https://www.weblancer.net{href}" if href else ""

                # ID из ссылки (например ...-1265596/)
                project_id = None
                if href:
                    # Ищем цифры в конце ссылки
                    match = re.search(r'-(\d+)/?$', href)
                    if match:
                        project_id = match.group(1)

                # Цена
                price_elem = card.find('span', class_='text-green-600')
                price = price_elem.text.strip() if price_elem else "Цена не указана"

                # Описание
                desc_elem = card.find('p', class_='text-gray-600')
                description = desc_elem.text.strip() if desc_elem else ""

                if not project_id:
                    print(f"⚠️ [Weblancer] Не удалось извлечь ID из: {href}")
                    continue

                # Сохраняем в БД
                insert_into_db(title, price, description, link, project_id, source=self.source)

                projects.append({
                    "title": title,
                    "price": price,
                    "description": description,
                    "link": link,
                    "project_id": project_id,
                    "source": self.source
                })

                print(f"✅ [Weblancer] {title[:50]}... | {price}")

            except Exception as e:
                print(f"⚠️ [Weblancer] Ошибка парсинга: {e}")
                continue

        print(f"📊 [Weblancer] Страница {page}: найдено {len(projects)} проектов")
        return projects

    async def get_total_pages(self, session: aiohttp.ClientSession, html: str) -> int:
        """Определение количества страниц"""
        soup = BeautifulSoup(html, 'html.parser')

        # Ищем пагинацию
        pagination = soup.find('nav', {'aria-label': 'Pagination'})
        if pagination:
            page_links = pagination.find_all('a', class_='px-3')
            for link in page_links:
                text = link.text.strip()
                if text.isdigit():
                    return int(text)

        return 1

    async def run(self, pages: int = 2) -> List[Dict]:
        """Запуск парсера Weblancer"""
        print(f"\n🚀 Запуск парсера Weblancer ({pages} страниц)")
        all_projects = []

        async with aiohttp.ClientSession() as session:
            # Загружаем первую страницу
            first_html = await self.fetch(session, self.base_url)
            if not first_html:
                print("❌ [Weblancer] Не удалось загрузить первую страницу")
                return []

            # Определяем реальное количество страниц
            total_pages = await self.get_total_pages(session, first_html)
            pages_to_parse = min(pages, total_pages)

            # Парсим первую страницу
            projects = self.parse_projects(first_html, 1)
            all_projects.extend(projects)

            # Парсим остальные страницы
            for page in range(2, pages_to_parse + 1):
                url = f"{self.base_url}?page={page}"
                html = await self.fetch(session, url)
                if html:
                    projects = self.parse_projects(html, page)
                    all_projects.extend(projects)
                await asyncio.sleep(0.5)

        print(f"✅ [Weblancer] Собрано {len(all_projects)} проектов")
        return all_projects


# Для тестирования
async def main():
    parser = WeblancerParser()
    projects = await parser.run(pages=1)
    print(f"\n📦 Найдено проектов: {len(projects)}")

if __name__ == "__main__":
    asyncio.run(main())