import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from agno.agent import Agent
from agno.models.openrouter import OpenRouter

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools

from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType

from agno.db.sqlite import SqliteDb

from config1.config import Config, load_config


config : Config = load_config()

API_KEY = config.agent.token
ID_MODEL = config.agent.id_model
BOT_TOKEN = config.bot.token


# создаём память агента в базе данных SQLite
db = SqliteDb(db_file="data_fin.db")

# локальный эмбеддер Agno на базе SentenceTransformers
embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",
)

# используем LanceDB как локальную векторную базу с гибридным поиском
vector_db = LanceDb(
    table_name="text_documents",    # имя таблицы для эмбеддингов
    uri="knowledge_fin",            # локальная папка/URI для LanceDB
    search_type=SearchType.hybrid,  # гибридный поиск: по смыслу + по ключевым словам
    embedder=embedder               # подключаем эмбеддер
)

knowledge = Knowledge(vector_db=vector_db)


# добавляем в базу знаний книгу "Алиса в Стране Чудес" :)
knowledge.add_content(
    url="https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt",
    skip_if_exists=True
)


agent = Agent(model=OpenRouter(id=ID_MODEL, api_key=API_KEY),
                description="Ты - дружелюбный помощник, который при необходимости пользуется интернетом",

                tools=[
                  DuckDuckGoTools(),       # инструмент поиска DuckDuckGo
                  Newspaper4kTools(),      # чтение страниц в интернете
                  CalculatorTools(),       # калькулятор для точных вычислений
                  YFinanceTools()          # финансовые инструменты от Yahoo
                ],
                session_id="agent",
                db=db,
                add_history_to_context=True,
                num_history_runs=0,
                knowledge=knowledge,
                search_knowledge=True,

                #debug_mode=True,
                #debug_level=1,
              )


bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def message(message: Message):
    user_text = message.text

    response = agent.run(user_text).content.strip()

    await message.answer(text=response)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())