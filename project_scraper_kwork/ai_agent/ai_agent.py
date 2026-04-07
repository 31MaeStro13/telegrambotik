from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.chroma import ChromaDb

from config.config import Config, load_config

config: Config = load_config()

API_KEY = config.ai.token
ID_MODEL = config.ai.id_model

# Настраиваем векторную БД (такая же, как в парсере)
embedder = SentenceTransformerEmbedder(id="all-MiniLM-L6-v2")


vector_db = ChromaDb(
    collection_name="kwork_projects",
    path="./chroma_db",  # путь к твоей ChromaDB
    embedder=embedder
)

knowledge_base = Knowledge(
    name="Kwork Projects",
    vector_db=vector_db
)

# Агент с доступом к базе знаний
recommendation_agent = Agent(
    model=OpenRouter(id=ID_MODEL, api_key=API_KEY),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Ты — карьерный ментор.",
        "Твоя задача: изучить профиль студента и найти в базе знаний подходящие проекты.",
        "Используй поиск по базе знаний, чтобы получить релевантные проекты.",
        "Выбери лучшие варианты и объясни, почему они подходят под стек и цели студента.",
        "Если проект длинный — выдели ключевые навыки жирным.",
        "Пиши дружелюбно и мотивирующе."
    ]
)
