# backend/app/core/config.py
from pydantic_settings import BaseSettings   # ← 変更ポイント
from openai import OpenAI

class Settings(BaseSettings):
    # CORS 用の許可ドメイン
    CORS_ORIGINS: list[str] = ["*"]

    # 例：OpenAI キーもここで読み込めます
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"       # ここに書けば自動で読んでくれる
        case_sensitive = True

settings = Settings()

openai_client = OpenAI(
    api_key=settings.OPENAI_API_KEY      # None なら環境変数で自動取得
)