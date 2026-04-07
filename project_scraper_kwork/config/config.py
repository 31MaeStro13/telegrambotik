from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin: str

@dataclass
class LogSetting:
    level: str
    format: str

@dataclass
class BaseData:
    user: str
    password: any
    host: str
    database: str
    port: int

@dataclass
class AiAgent:
    token: str
    id_model: str

@dataclass
class Config:
    bot: TgBot
    log: LogSetting
    data: BaseData
    ai: AiAgent

def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env()

    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN'),
            admin=env('ADMIN_ID')
        ),
        log=LogSetting(
            level=env('LOG_LEVEL'),
            format=env('LOG_FORMAT')
        ),
        data=BaseData(
            user=env('DB_USER'),
            password=env('DB_PASSWORD'),
            host=env('DB_HOST', ''),
            database=env('DB_DATABASE', None),
            port=env.int('DB_PORT')
        ),
        ai=AiAgent(
            token=env('OPENAI_API_KEY'),
            id_model=env('ID_MODEL')
        ),
    )