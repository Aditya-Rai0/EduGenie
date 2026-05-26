from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Environment
    ENVIRONMENT: str = "development"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # GCP
    GCP_PROJECT_ID: str = ""
    GCP_REGION: str = "us-central1"
    GCP_STORAGE_BUCKET: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_ORG_ID: str = ""

    # ElevenLabs
    ELEVENLABS_API_KEY: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_CONNECT_CLIENT_ID: str = ""

    # SendGrid
    SENDGRID_API_KEY: str = ""

    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""

    # Algolia
    ALGOLIA_APP_ID: str = ""
    ALGOLIA_API_KEY: str = ""
    ALGOLIA_INDEX_NAME: str = "edugenie_courses"

    # PostHog
    POSTHOG_API_KEY: str = ""

    # Langfuse
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/edugenie"

    # App
    APP_NAME: str = "EduGenie API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
