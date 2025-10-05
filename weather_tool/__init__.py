# __init__.py - Expõe as classes principais
"""
Weather Tool - Ferramenta de clima para agentes IA

Uso básico:
    >>> from weather_tool import WeatherTool
    >>> tool = WeatherTool()
    >>> data = tool.get_weather("São Paulo")
    >>> print(data.to_display_format())
"""

from .client import WeatherTool
from .models import WeatherData, WeatherMain, WeatherDescription
from .exceptions import (
    WeatherAPIError,
    CityNotFoundError,
    InvalidAPIKeyError,
    NetworkError
)
from .settings import WeatherConfig, get_settings

# Define o que é exportado quando fazem: from weather_tool import *
__all__ = [
    "WeatherTool",
    "WeatherData",
    "WeatherMain",
    "WeatherDescription",
    "WeatherAPIError",
    "CityNotFoundError",
    "InvalidAPIKeyError",
    "NetworkError",
    "WeatherConfig",
    "get_settings",
]

__version__ = "1.0.0"
