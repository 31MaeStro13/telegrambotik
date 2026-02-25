# В НАЧАЛЕ файла aiagent.py добавьте:
import sys
import os

# Добавляем родительскую директорию в путь Python
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Теперь импортируем
from config.config import Config, load_config

from agno.agent import Agent
from agno.models.openrouter import OpenRouter

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools

from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType

from agno.db.sqlite import SqliteDb


config: Config = load_config()

ID_MODEL = config.agnet.id_model
API_KEY = config.agnet.token

db = SqliteDb(db_file="data.db")

embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",
)

vector_db = LanceDb(
    table_name="psychology_resources",
    uri="therapy_documents_db",
    search_type=SearchType.hybrid,
    embedder=embedder,
)

knowledge = Knowledge(
    name="therapy_resources",
    vector_db=vector_db,
    description="База психологических техник, информации о ментальном здоровье и ресурсов поддержки"
)

# добавляем в базу знаний книгу "Алиса в Стране Чудес" :)
# nowledge.add_content(
#    url="https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt",
#   skip_if_exists=True
#)

agent = Agent(model=OpenRouter(
        id=ID_MODEL,  # Модель для reasoning
        api_key=API_KEY,
    ),

           instructions=[
        "ТЫ: Персональный коуч-помощник по имени ВЕО.",
        "СТИЛЬ: Дружелюбный, поддерживающий, но не слишком формальный.",

        "ПРАВИЛА ОБЩЕНИЯ:",
        "1. Приветствуй пользователя только ОДИН РАЗ в начале диалога",
        "2. Запоминай информацию о пользователе: имя, увлечения, профессию",
        "3. Используй контекст из предыдущих сообщений",
        "4. Не повторяй одни и те же фразы",
        "5. Будь естественным, как человек",

        "О ТЕБЕ:",
        "- Ты можешь создавать персонализированные мантры",
        "- У тебя есть доступ к базе знаний с шаблонами",
        "- Ты можешь синтезировать голос (если пользователь пришлет голосовое)",
        "- Сегодня: 10 февраля 2026 года (используй эту дату)",

        "ФОРМАТ:",
        "- Отвечай кратко, но содержательно",
        "- Задавай уточняющие вопросы если нужно",
        "- Предлагай создать мантру когда уместно",
        "- Не напоминай о своих возможностях слишком часто",
    ],

    description="Персональный коуч для создания мантр",

                tools=[
                  DuckDuckGoTools(),       # инструмент поиска DuckDuckGo
                  Newspaper4kTools(),      # чтение страниц в интернете
                ],
                session_id="agent",
                db=db,
                add_history_to_context=True,
                num_history_runs=5,
                knowledge=knowledge,
                search_knowledge=True,

                #debug_mode=True,
                #debug_level=1,
              )


if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content)