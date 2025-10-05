import pytest
import os
from unittest.mock import patch
from weather_tool.settings import WeatherConfig, get_settings


def test_config_creation():
    """Testa criação de config com valores válidos"""
    with patch.dict(os.environ, {"DISABLE_ENV_LOAD": "1"}, clear=True):
        config = WeatherConfig(
            api_key="test_key_12345678901234567890",
            base_url="https://api.test.com",
            timeout=5,
        )
        assert config.api_key == "test_key_12345678901234567890"
        assert config.timeout == 5
        assert "test.com" in config.base_url


def test_config_validation():
    """Testa validação de API key pelo get_settings()"""
    with patch.dict(os.environ, {"DISABLE_ENV_LOAD": "1"}, clear=True):
        with pytest.raises(ValueError, match="API key não configurada"):
            get_settings()

