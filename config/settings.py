from pathlib import Path
from typing import Optional, Literal
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "Auto Web Test"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 路径配置
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOGS_DIR: Path = BASE_DIR / "logs"

    # 数据库通用配置
    DB_TYPE: Literal["mysql", "postgresql"] = "mysql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "test_db"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # 通过拼接属性自动生成 SQLAlchemy URL
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "mysql":
            return (
                f"mysql+pymysql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        elif self.DB_TYPE == "postgresql":
            return (
                f"postgresql+psycopg2://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        raise ValueError(f"Unsupported DB_TYPE: {self.DB_TYPE}")

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
