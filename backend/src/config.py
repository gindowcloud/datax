import os
from pydantic import BaseSettings
from dotenv import load_dotenv
from urllib.parse import quote_plus as quote

load_dotenv()


class Config(BaseSettings):

    # 接口地址
    prefix: str = os.getenv("APP_PREFIX", '/api/v1')

    # 数据库连接
    db_connection = os.getenv("DB_CONNECTION", "sqlite")
    db_host = os.getenv("DB_HOST", "")
    db_port = os.getenv("DB_PORT", "")
    db_username = os.getenv("DB_USERNAME", "")
    db_password = os.getenv("DB_PASSWORD", "")
    db_database = os.getenv("DB_DATABASE", "data/datax.db")

    def get_alchemy_url(self):
        if self.db_connection == "sqlite":
            return f"{self.db_connection}:///{self.db_database}"
        else:
            return f"{self.db_connection}://" \
                   f"{self.db_username}:{quote(self.db_password)}@{self.db_host}:{self.db_port}/" \
                   f"{self.db_database}"

    # 执行参数
    python = os.getenv("PYTHON", "python")
    datax = os.getenv("DATAX", "/datax/bin/datax.py")


config = Config()
