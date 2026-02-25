from typing import List, Optional
from pydantic import BaseModel, Field

from agno.team import Team
from agno.agent import Agent, RunOutput
from agno.models.openrouter import OpenRouter
from agno.db.sqlite import SqliteDb
from agno.learn import (
    LearningMachine,
    LearningMode,
    LearnedKnowledgeConfig,
    )
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools
from agno.utils.pprint import pprint_run_response

from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType


from config1.config import Config, load_config

config: Config = load_config()

API_KEY = config.agent.token
ID_MODEL = config.agent.id_model


db = SqliteDb(db_file="data.db")

embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",
)

vector_db = LanceDb(
    table_name="learnings",
    uri="knowledge_fin",
    search_type=SearchType.hybrid,
    embedder=embedder,
)

knowledge = Knowledge(
    name="Agent Learnings",
    vector_db=vector_db
)

friend = Agent(
    name="friend",
    role="Мы с тобой просто дружески беседуем, у тебя есть память и ты будешь хорошо меня знать",
    db=db,
    add_history_to_context=False,
    learning=LearningMachine(
        knowledge=knowledge,
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.AGENTIC),
    ),
    markdown=True,
)

news_agent = Agent(
    name='News agent',
    role='Get trending tech news from HackerNews and Get stock prices and financial data',
    tools=[HackerNewsTools(),YFinanceTools()]
)

team = Team (
    name="Research Team",
    members=[friend, news_agent],
    model=OpenRouter(id=ID_MODEL, api_key=API_KEY),
    instructions="Delegate to the appropriate agent based on the request."
)


if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", team.run(question).content)