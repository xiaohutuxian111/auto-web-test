from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

from config.database import database_settings


class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "Auto Web Test"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 路径配置
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOGS_DIR: Path = BASE_DIR / "logs"

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # 测试配置
    TEST_TIMEOUT: int = 30_000
    RETRY_COUNT: int = 3

    # 浏览器配置
    BROWSER_TYPE: str = "chrome"
    HEADLESS: bool = False

    # 代理配置
    PROXY_URL: Optional[str] = None

    # 飞书配置
    FEISHU_WEBHOOK_URL: str = ''
    FEISHU_APP_ID: str = ''
    FEISHU_APP_SECRET: str = ''

    # 数据库配置兼容入口。新代码优先从 config.database 导入 database_settings。
    @property
    def DB_TYPE(self):
        return database_settings.DB_TYPE

    @property
    def DB_HOST(self):
        return database_settings.DB_HOST

    @property
    def DB_PORT(self):
        return database_settings.DB_PORT

    @property
    def DB_USER(self):
        return database_settings.DB_USER

    @property
    def DB_PASSWORD(self):
        return database_settings.DB_PASSWORD

    @property
    def DB_NAME(self):
        return database_settings.DB_NAME

    @property
    def DB_ECHO(self):
        return database_settings.DB_ECHO

    @property
    def DB_POOL_SIZE(self):
        return database_settings.DB_POOL_SIZE

    @property
    def DB_MAX_OVERFLOW(self):
        return database_settings.DB_MAX_OVERFLOW

    @property
    def DB_POOL_RECYCLE(self):
        return database_settings.DB_POOL_RECYCLE

    @property
    def DB_POOL_PRE_PING(self):
        return database_settings.DB_POOL_PRE_PING

    @property
    def DATABASE_URL(self):
        return database_settings.DATABASE_URL

    # Pydantic 配置
    model_config = {
        "env_file": f"{BASE_DIR}/.env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


# 创建全局设置实例
settings = Settings()

if __name__ == '__main__':
    print(settings.DATABASE_URL)
