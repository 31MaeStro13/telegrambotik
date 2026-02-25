from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseCongig:
    name: str
    host: str
    user: str
    password: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class Config:
    bot: TgBot
    db: DatabaseCongig

def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env()

    return Config(
        bot=TgBot(
            token=env('TOKEN_API'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseCongig(
            name=env('DB_NAME'),
            host=env('DB_HOST'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD')
        )
    )
