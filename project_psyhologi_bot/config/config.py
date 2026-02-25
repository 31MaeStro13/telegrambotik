from environs import Env
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str
    admin: str

@dataclass
class Log:
    level: str
    formatlog: str

@dataclass
class AiAgent:
    token: str
    id_model: str

@dataclass
class Config:
    bot: TgBot
    log: Log
    agnet: AiAgent

def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env()

    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN'),
            admin=env('ADMIN_IDS')
        ),
        log=Log(
            level=env('LOG_LEVEL'),
            formatlog=env('LOG_FORMAT')
        ),
        agnet=AiAgent(
            token=env('OPENAI_API_KEY'),
            id_model=env('ID_MODEL')
        )
    )