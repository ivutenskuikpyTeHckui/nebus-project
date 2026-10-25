import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ClientDBConfig:
    HOST: str = os.environ.get("CLIENT_DB_HOST")
    USERNAME: str = os.environ.get("CLIENT_DB_USERNAME")
    PASSWORD: str = os.environ.get("CLIENT_DB_PASSWORD")
    PORT: str = os.environ.get("CLIENT_DB_PORT")
    DATABASE: str = os.environ.get("CLIENT_DB_DATABASE")


@dataclass(frozen=True)
class AuthConfig:
    API_KEY: str = os.environ.get("API_KEY", "dev-api-key")


@dataclass(frozen=True)
class RabbitConfig:
    URL: str = os.environ.get(
        "RABBITMQ_URL",
        "amqp://root:root@rabbitmq:5672/",
    )


@dataclass(frozen=True)
class WebhookConfig:
    TIMEOUT_SECONDS: float = float(os.environ.get("WEBHOOK_TIMEOUT_SECONDS", "10"))
    MAX_ATTEMPTS: int = 3


@dataclass(frozen=True)
class Config:
    AUTH: AuthConfig = AuthConfig()
    CLIENT_DB: ClientDBConfig = ClientDBConfig()
    RABBITMQ: RabbitConfig = RabbitConfig()
    WEBHOOK: WebhookConfig = WebhookConfig()


CONFIG = Config()
