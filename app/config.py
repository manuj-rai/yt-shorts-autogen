from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    env: str = Field(default="production", alias="ENV")
    app_name: str = Field(default="yt-shorts-autogen", alias="APP_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_pass: str = Field(default="postgres", alias="DB_PASS")
    db_name: str = Field(default="postgres", alias="DB_NAME")

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    pexels_api_key: str | None = Field(default=None, alias="PEXELS_API_KEY")
    azure_tts_key: str | None = Field(default=None, alias="AZURE_TTS_KEY")
    azure_tts_region: str | None = Field(default=None, alias="AZURE_TTS_REGION")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    youtube_client_secret_json: str | None = Field(default=None, alias="YOUTUBE_CLIENT_SECRET_JSON")
    youtube_token_json: str | None = Field(default=None, alias="YOUTUBE_TOKEN_JSON")

    channel_niche: str = Field(default="productivity,tech,learning", alias="CHANNEL_NICHE")
    default_lang: str = Field(default="en", alias="DEFAULT_LANG")
    default_locale: str = Field(default="US", alias="DEFAULT_LOCALE")
    default_timezone: str = Field(default="Asia/Kolkata", alias="DEFAULT_TIMEZONE")

    media_dir: str = Field(default="/data/media", alias="MEDIA_DIR")
    renders_dir: str = Field(default="/data/renders", alias="RENDERS_DIR")
    license_ledger: str = Field(default="/data/licenses.json", alias="LICENSE_LEDGER")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
os.makedirs(settings.media_dir, exist_ok=True)
os.makedirs(settings.renders_dir, exist_ok=True)
