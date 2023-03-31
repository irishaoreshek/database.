from dataclasses import dataclass

from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class Cat:
    token: str

@dataclass
class Config:
    database: Database
    tgBot: TgBot
    cat: Cat

def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(database=Database(
        host=env('HOST'),
        port=int(env('PORT')),
        user=env('USER'),
        password=env('PASSWORD'),
        database=env('DATABASE')),
        tgBot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ID_ADMINS')))),
        cat=Cat(token=env('CAT_TOKEN')))