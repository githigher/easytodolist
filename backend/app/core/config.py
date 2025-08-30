# backend/app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库URL
    # 格式: "mysql+mysqlclient://<user>:<password>@<host>:<port>/<dbname>"
    # 示例: "mysql+mysqlclient://root:your_password@127.0.0.1:3306/todo_db"
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:123456@localhost/todo_db"

    # JWT 配置
    SECRET_KEY: str = "a_very_secret_key_that_should_be_changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()