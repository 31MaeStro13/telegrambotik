"""Базовый класс для всех парсеров"""
import asyncio
import aiohttp
import time
from typing import List, Dict, Optional

class BaseParser:
    """Базовый класс парсера"""

    def __init__(self, source_name: str):
        self.source = source_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }

    async def fetch(self, session: aiohttp.ClientSession, url: str, retry: int = 3) -> Optional[str]:
        """Асинхронный GET запрос с повторными попытками"""
        for attempt in range(retry):
            try:
                async with session.get(url, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"⚠️ [{self.source}] Статус {response.status} для {url}, попытка {attempt + 1}")
            except Exception as e:
                print(f"❌ [{self.source}] Ошибка: {e}, попытка {attempt + 1}")

            if attempt < retry - 1:
                await asyncio.sleep(2 ** attempt)

        return None

    async def run(self, pages: int = 2) -> List[Dict]:
        """Запуск парсера - нужно переопределить"""
        raise NotImplementedError