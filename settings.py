from typing import List, Dict

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    DEBUG: bool
    ALLOWED_HOSTS: str

    ENGINE: str
    NAME_DB: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    SMTP_SERVER: str
    SALE_EMAIL: str
    SALE_PASSWORD_EMAIL: str
    SUBJECT: str
    BODY: str
    PORT_TLS: int
    TO: str

    FROM_APP: str
    PASSWORD_APP: str
    DEPARTMENT: Dict[str, List[str]]

    # CORS_ORIGIN_ALLOW_ALL: bool
    # CORS_ALLOW_CREDENTIALS: bool
    # CORS_ALLOW_HEADERS: str
    # CSRF_COOKIE_SECURE: bool

    # EMAIL_HOST: str
    # EMAIL_PORT: int
    # DEFAULT_FROM_EMAIL: str
    # EMAIL_HOST_USER: str
    # EMAIL_HOST_PASSWORD: str
    # EMAIL_USE_TLS: bool
    # EMAIL_USE_SSL: bool

    # SOCIAL_AUTH_FACEBOOK_KEY: str
    # SOCIAL_AUTH_FACEBOOK_SECRET: str
    # SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: str
    # SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: str

    # CELERY_BROKER_URL: str
    # CELERY_RESULT_BACKEND: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
