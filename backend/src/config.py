import os
from pydantic import BaseSettings
from dotenv import load_dotenv
from urllib.parse import quote_plus as quote

load_dotenv()


class Config(BaseSettings):

    # 接口地址
    prefix: str = os.getenv("APP_PREFIX", '/')

    # 数据库连接
    db_connection = os.getenv("DB_CONNECTION")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_database = os.getenv("DB_DATABASE")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")

    def get_alchemy_url(self):
        return f"{self.db_connection}://" \
               f"{self.db_username}:{quote(self.db_password)}@{self.db_host}:{self.db_port}/" \
               f"{self.db_database}"

    # Redis
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_db = os.getenv("REDIS_DB", 0)
    redis_password = os.getenv("REDIS_PASSWORD")

    def get_redis_url(self):
        return f"redis://{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}?encoding=utf-8"


config = Config()
