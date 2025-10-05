# client.py - Versão COMPLETA com logs estratégicos
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from loguru import logger
from requests.exceptions import HTTPError, Timeout, RequestException

from .settings import get_settings, WeatherConfig
from .models import WeatherData, WeatherMain, WeatherDescription
from .exceptions import WeatherAPIError, CityNotFoundError, InvalidAPIKeyError, NetworkError


class WeatherTool:
    """Ferramenta de clima com cache e logging completo"""
    
    def __init__(self, config: Optional[WeatherConfig] = None):
        """Inicializa a ferramenta"""
        self.config = config or get_settings()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_duration = timedelta(minutes=10)
        
        # 🎯 LOG: Inicialização (importante para debug)
        logger.info(f"WeatherTool inicializado")
        logger.debug(f"Cache configurado: {self._cache_duration.total_seconds()}s")
    
    def get_weather(self, city: str) -> WeatherData:
        """Busca clima com cache automático"""
        
        # 🎯 LOG: Início da operação
        logger.info(f"Requisição de clima para: {city}")
        
        # Validação
        if not city or not city.strip():
            logger.error("Cidade vazia fornecida")
            raise WeatherAPIError("Nome da cidade não pode estar vazio")
        
        city_key = city.lower().strip()
        
        # 1. Verifica cache
        if city_key in self._cache:
            cache_entry = self._cache[city_key]
            if self._is_cache_valid(cache_entry):
                # 🎯 LOG: Cache hit (sucesso)
                logger.success(f"✓ Cache hit: {city}")
                return cache_entry["data"]
            else:
                # 🎯 LOG: Cache expirado
                logger.debug(f"Cache expirado para {city}, removendo...")
                del self._cache[city_key]
        
        # 🎯 LOG: Cache miss (vai buscar da API)
        logger.info(f"Cache miss: buscando {city} da API")
        
        # 2. Busca da API
        weather_data = self._fetch_from_api(city)
        
        # 3. Salva no cache
        self._cache[city_key] = {
            "data": weather_data,
            "timestamp": datetime.now()
        }
        
        # 🎯 LOG: Sucesso final
        logger.success(f"✓ Dados obtidos e salvos no cache: {city}")
        
        return weather_data
    
    def _fetch_from_api(self, city: str) -> WeatherData:
        """Busca dados da API OpenWeatherMap"""
        
        params = {
            "q": city.strip(),
            "appid": self.config.api_key,
            "units": "metric",
            "lang": "pt_br"
        }
        
        try:
            # 🎯 LOG: Requisição HTTP
            logger.debug(f"GET {self.config.base_url} | city={city}")
            
            response = requests.get(
                self.config.base_url,
                params=params,
                timeout=self.config.timeout
            )
            
            # 🎯 LOG: Status da resposta
            logger.debug(f"Status code: {response.status_code}")
            
            response.raise_for_status()
            data = response.json()
            
            # Parse e retorno
            weather_data = self._parse_response(data)
            return weather_data
            
        except HTTPError as e:
            # 🎯 LOG: Erro HTTP específico
            if response.status_code == 404:
                logger.warning(f"Cidade não encontrada: {city}")
                raise CityNotFoundError(f"Cidade '{city}' não encontrada")
            elif response.status_code == 401:
                logger.error("API key inválida ou expirada")
                raise InvalidAPIKeyError("API key inválida")
            else:
                logger.error(f"Erro HTTP {response.status_code}: {e}")
                raise WeatherAPIError(f"Erro na API: {e}")
        
        except Timeout:
            # 🎯 LOG: Timeout
            logger.error(f"Timeout na requisição para {city}")
            raise NetworkError(f"Timeout ao buscar {city}")
        
        except RequestException as e:
            # 🎯 LOG: Erro de rede genérico
            logger.error(f"Erro de conexão: {e}")
            raise NetworkError(f"Erro de conexão: {e}")
        
        except Exception as e:
            # 🎯 LOG: Erro inesperado
            logger.exception(f"Erro inesperado ao buscar {city}")
            raise WeatherAPIError(f"Erro inesperado: {e}")
    
    def _parse_response(self, data: Dict[str, Any]) -> WeatherData:
        """Converte resposta da API para modelo Pydantic"""
        
        try:
            # 🎯 LOG: Início do parsing
            logger.debug(f"Parseando resposta para {data.get('name', 'unknown')}")
            
            # Extrai dados
            main = WeatherMain(
                temp=data["main"]["temp"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                humidity=data["main"]["humidity"],
                feels_like=data["main"]["feels_like"]
            )
            
            weather_list = [
                WeatherDescription(
                    main=w["main"],
                    description=w["description"],
                    icon=w["icon"]
                ) for w in data.get("weather", [])
            ]
            
            weather_data = WeatherData(
                city_name=data["name"],
                country=data.get("sys", {}).get("country"),
                main=main,
                weather=weather_list
            )
            
            # 🎯 LOG: Parse bem-sucedido
            logger.debug(f"Parse concluído: {weather_data.city_name}")
            
            return weather_data
            
        except KeyError as e:
            # 🎯 LOG: Falta de campo esperado
            logger.error(f"Campo ausente na resposta da API: {e}")
            raise WeatherAPIError(f"Dados incompletos da API: campo {e} não encontrado")
        
        except Exception as e:
            # 🎯 LOG: Erro no parsing
            logger.exception(f"Erro ao processar resposta da API")
            raise WeatherAPIError(f"Erro ao processar dados: {e}")
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Verifica se cache ainda é válido"""
        cached_time = cache_entry.get("timestamp")
        if not cached_time:
            return False
        
        age = datetime.now() - cached_time
        return age < self._cache_duration
    
    # 🎯 MÉTODOS PARA IA
    def get_weather_for_agent(self, city: str) -> Dict[str, Any]:
        """Formato otimizado para LangChain/LangGraph"""
        logger.info(f"Requisição de agente IA para: {city}")
        weather = self.get_weather(city)
        return weather.to_agent_format()
    
    def display_weather(self, city: str) -> str:
        """Formato legível para humanos"""
        weather = self.get_weather(city)
        return weather.to_display_format()
    
    # 🎯 MÉTODOS DE GERENCIAMENTO DO CACHE
    def get_cache_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o cache"""
        valid = sum(1 for entry in self._cache.values() if self._is_cache_valid(entry))
        
        info = {
            "total_cities": len(self._cache),
            "valid_entries": valid,
            "expired_entries": len(self._cache) - valid,
            "cache_duration_minutes": self._cache_duration.total_seconds() / 60,
            "cached_cities": list(self._cache.keys())
        }
        
        logger.info(f"Cache info: {valid}/{len(self._cache)} entradas válidas")
        return info
    
    def clear_cache(self) -> None:
        """Limpa todo o cache"""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"Cache limpo: {count} entradas removidas")