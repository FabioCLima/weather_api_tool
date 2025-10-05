# exceptions.py
class WeatherAPIError(Exception):
    """Erro base para problemas com a API"""
    pass

class CityNotFoundError(WeatherAPIError):
    """Cidade não encontrada"""
    pass

class InvalidAPIKeyError(WeatherAPIError):
    """API key inválida"""
    pass

class NetworkError(WeatherAPIError):
    """Erro de conexão"""
    pass