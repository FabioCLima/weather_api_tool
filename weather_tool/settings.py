"""Configurações do Weather Tool"""
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class WeatherConfig(BaseSettings):
    """Configuração simples para o Weather Tool"""

    model_config = SettingsConfigDict(
        env_file=".env" if not os.getenv("DISABLE_ENV_LOAD") else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Configuração da API
    api_key: Optional[str] = Field(
        default=None,
        description="OpenWeather API key",
        alias="OPENWEATHER_API_KEY"
    )

    base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5/weather",
        description="URL base da API do clima"
    )

    timeout: int = Field(
        default=10,
        ge=1,
        le=30,
        description="Timeout da requisição em segundos"
    )


def get_settings() -> WeatherConfig:
    """Carrega as configurações do .env e valida"""
    config = WeatherConfig()

    if not config.api_key or not config.api_key.strip():
        raise ValueError("API key não configurada. Adicione OPENWEATHER_API_KEY no .env")

    logger.success(f"Config carregada! API key: ...{config.api_key[-4:]}")
    return config
