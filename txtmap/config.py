from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn = 'postgres://postgres@localhost:5432'


config = Config()
