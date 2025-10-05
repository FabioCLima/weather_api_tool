#!/usr/bin/env python3
"""
Script para configurar a estrutura do projeto Weather Tool
Execute na raiz do projeto: python setup_project.py
"""
import os
from pathlib import Path
import shutil

def create_project_structure():
    """Cria a estrutura completa do projeto"""
    
    print("🔨 Criando estrutura do projeto Weather Tool...")
    
    # Diretório raiz
    root = Path.cwd()
    
    # 1. Criar diretórios principais
    directories = [
        "weather_tool",
        "examples", 
        "tests",
        "logs"  # Para os logs do loguru
    ]
    
    for dir_name in directories:
        dir_path = root / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Criado: {dir_name}/")
    
    # 2. Criar __init__.py no weather_tool
    init_file = root / "weather_tool" / "__init__.py"
    init_content = '''"""Weather Tool - Ferramenta simples de clima"""
from .settings import WeatherConfig, get_settings

__version__ = "0.1.0"
__all__ = ["WeatherConfig", "get_settings"]

# Depois adicionar:
# from .models import WeatherData
# from .client import WeatherTool
'''
    init_file.write_text(init_content)
    print("✅ Criado: weather_tool/__init__.py")
    
    # 3. Mover settings.py se existir em src/
    old_settings = root / "src" / "weather_tool" / "settings.py"
    new_settings = root / "weather_tool" / "settings.py"
    
    if old_settings.exists():
        shutil.copy2(old_settings, new_settings)
        print(f"✅ Copiado: settings.py de src/ para weather_tool/")
    elif not new_settings.exists():
        # Criar settings.py básico se não existir
        settings_content = '''"""Configurações do Weather Tool"""
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
                "⚠️  API Key não encontrada!\\n"
                "Por favor:\\n"
                "1. Crie um arquivo .env na raiz\\n"
                "2. Adicione: OPENWEATHER_API_KEY=sua_chave\\n"
            )
            raise ValueError("API key não configurada")
            
        logger.success(f"Config carregada! API key: ...{config.api_key[-4:]}")
        return config
        
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {e}")
        raise
'''
        new_settings.write_text(settings_content)
        print("✅ Criado: weather_tool/settings.py")
    
    # 4. Criar models.py stub
    models_file = root / "weather_tool" / "models.py"
    if not models_file.exists():
        models_content = '''"""Modelos de dados do Weather Tool"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WeatherData(BaseModel):
    """Modelo placeholder - implementar depois"""
    city: str = Field(..., description="Nome da cidade")
    temperature: float = Field(..., description="Temperatura em Celsius")
    description: str = Field(..., description="Descrição do clima")
    
    def to_agent_format(self) -> dict:
        """Formato para agentes IA"""
        return {
            "location": self.city,
            "temp_celsius": self.temperature,
            "conditions": self.description
        }
'''
        models_file.write_text(models_content)
        print("✅ Criado: weather_tool/models.py (stub)")
    
    # 5. Criar client.py stub
    client_file = root / "weather_tool" / "client.py"
    if not client_file.exists():
        client_content = '''"""Cliente principal do Weather Tool"""
from typing import Optional
from .settings import get_settings, WeatherConfig


class WeatherTool:
    """Ferramenta de clima - implementação principal"""
    
    def __init__(self, config: Optional[WeatherConfig] = None):
        """Inicializa a ferramenta"""
        self.config = config or get_settings()
        print(f"WeatherTool inicializado com API key: ...{self.config.api_key[-4:]}")
    
    def fetch_weather(self, city: str):
        """Busca dados do clima - implementar"""
        print(f"TODO: Buscar clima para {city}")
        return {"city": city, "temp": 25.0, "description": "Ensolarado"}
'''
        client_file.write_text(client_content)
        print("✅ Criado: weather_tool/client.py (stub)")
    
    # 6. Criar main.py
    main_file = root / "main.py"
    if not main_file.exists():
        main_content = '''#!/usr/bin/env python3
"""Entrada principal do Weather Tool"""

def main():
    """Executa o Weather Tool"""
    try:
        from weather_tool.settings import get_settings
        
        # Testa carregamento da config
        config = get_settings()
        print(f"✅ Weather Tool pronto!")
        print(f"   API Key: ...{config.api_key[-4:]}")
        print(f"   Timeout: {config.timeout}s")
        
        # TODO: Adicionar WeatherTool quando implementado
        # from weather_tool.client import WeatherTool
        # tool = WeatherTool()
        # tool.run_interactive()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\\nVerifique o arquivo .env!")

if __name__ == "__main__":
    main()
'''
        main_file.write_text(main_content)
        print("✅ Criado: main.py")
    
    # 7. Criar exemplo .env se não existir
    env_file = root / ".env"
    if not env_file.exists():
        env_example = root / ".env.example"
        env_content = """# Configurações do Weather Tool
# Copie para .env e adicione sua chave

# Obtenha em: https://openweathermap.org/api
OPENWEATHER_API_KEY=sua_chave_api_aqui

# Opcional
API_TIMEOUT=10
LOG_LEVEL=INFO
"""
        env_example.write_text(env_content)
        print("✅ Criado: .env.example (copie para .env e adicione sua chave)")
    
    # 8. Criar test básico
    test_file = root / "tests" / "test_basic.py"
    if not test_file.exists():
        test_content = '''"""Testes básicos do Weather Tool"""
import pytest
from weather_tool.settings import WeatherConfig


def test_config_creation():
    """Testa criação de config com valores válidos"""
    config = WeatherConfig(
        api_key="test_key_12345678901234567890",
        base_url="https://api.test.com",
        timeout=5
    )
    assert config.api_key == "test_key_12345678901234567890"
    assert config.timeout == 5
    assert "test.com" in config.base_url


def test_config_validation():
    """Testa validação de API key"""
    with pytest.raises(ValueError, match="API key"):
        WeatherConfig(api_key="")
    
    with pytest.raises(ValueError, match="muito curta"):
        WeatherConfig(api_key="123")
'''
        test_file.write_text(test_content)
        print("✅ Criado: tests/test_basic.py")
    
    print("\n📋 Estrutura criada com sucesso!")
    print("\n📁 Estrutura do projeto:")
    print("""
weather_api_tool/
├── weather_tool/
│   ├── __init__.py
│   ├── settings.py
│   ├── models.py (stub)
│   └── client.py (stub)
├── examples/
├── tests/
│   └── test_basic.py
├── main.py
└── .env.example
    """)
    
    print("\n🎯 Próximos passos:")
    print("1. Copie .env.example para .env e adicione sua API key")
    print("2. Execute: uv sync (ou pip install -e .)")
    print("3. Teste: python main.py")
    print("4. Implemente os stubs em models.py e client.py")


if __name__ == "__main__":
    create_project_structure()