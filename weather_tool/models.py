# models.py - Versão 2: COM VALIDAÇÃO
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class WeatherMain(BaseModel):
    """Dados principais de temperatura"""
    temp: float = Field(..., description="Temperatura em °C")
    temp_min: float
    temp_max: float
    humidity: int = Field(..., ge=0, le=100)  # Entre 0 e 100!
    feels_like: float
    
    @validator('temp', 'temp_min', 'temp_max')
    def validate_temperature(cls, v):
        """Valida se temperatura está em faixa razoável"""
        if not -50 <= v <= 60:
            raise ValueError(f'Temperatura {v}°C inválida')
        return round(v, 1)  # Arredonda para 1 casa decimal


class WeatherDescription(BaseModel):
    """Descrição do clima"""
    main: str  # Ex: "Clear", "Clouds"
    description: str  # Ex: "céu limpo"
    icon: str  # Código do ícone


class WeatherData(BaseModel):
    """Modelo completo de dados climáticos"""
    
    # Dados básicos
    city_name: str
    country: Optional[str] = None
    
    # Dados climáticos
    main: WeatherMain
    weather: list[WeatherDescription]
    
    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # 🎯 MÉTODOS ÚTEIS PARA IA
    def to_agent_format(self) -> dict:
        """Formato otimizado para agentes IA (LangChain/LangGraph)"""
        return {
            "location": {
                "city": self.city_name,
                "country": self.country
            },
            "temperature": {
                "current": self.main.temp,
                "min": self.main.temp_min,
                "max": self.main.temp_max,
                "feels_like": self.main.feels_like
            },
            "conditions": self.weather[0].description if self.weather else "unknown",
            "humidity": self.main.humidity,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_display_format(self) -> str:
        """Formato legível para humanos"""
        return f"""
🌡️ Clima em {self.city_name}
Temperatura: {self.main.temp}°C (sensação: {self.main.feels_like}°C)
Condições: {self.weather[0].description if self.weather else 'N/A'}
Umidade: {self.main.humidity}%
"""