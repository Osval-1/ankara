from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    API_BASE_URL: str = "http://localhost:8000/api/v1"

    WHATSAPP_WEBHOOK_SECRET: str = ""
    WHATSAPP_API_KEY: str = ""
    WHATSAPP_API_URL: str = "https://waba.360dialog.io/v1"

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBHOOK_SECRET: str = ""


settings = Settings()
