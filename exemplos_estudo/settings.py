"""Configurações do Weather Tool"""
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class WeatherConfig(BaseSettings):
    """Configuração simples para o Weather Tool"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Configuração da API
    api_key: str = Field(
        default="",
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
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Valida se a API key não está vazia"""
        if not v or not v.strip():
            raise ValueError("API key não pode estar vazia")
        
        if len(v) < 10:
            raise ValueError("API key parece muito curta")
        
        return v.strip()


def get_settings() -> WeatherConfig:
    """Carrega as configurações do .env"""
    try:
        config = WeatherConfig()
        
        if not config.api_key:
            logger.error(
                "⚠️  API Key não encontrada!\n"
                "Por favor:\n"
                "1. Crie um arquivo .env na raiz\n"
                "2. Adicione: OPENWEATHER_API_KEY=sua_chave\n"
            )
            raise ValueError("API key não configurada")
            
        logger.success(f"Config carregada! API key: ...{config.api_key[-4:]}")
        return config
        
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {e}")
        raise
