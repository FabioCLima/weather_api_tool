"""
weather_for_agents.py
=====================

Interface SIMPLES para agentes IA usarem o weather_tool.

O agente importa este arquivo e chama as funções.
Todas retornam dados estruturados (dict/JSON) prontos para processamento.

Uso pelo agente:
    from weather_for_agents import get_weather, compare_weather
    
    # Busca clima de uma cidade
    result = get_weather("São Paulo")
    
    # Compara múltiplas cidades
    comparison = compare_weather(["Rio", "São Paulo", "Brasília"])
"""

from typing import Dict, Any, List, Optional
from weather_tool import WeatherTool, CityNotFoundError, WeatherAPIError
from loguru import logger

# Instância global (singleton) - criada uma vez, usada sempre
_weather_tool = None

def _get_tool() -> WeatherTool:
    """Retorna instância singleton do WeatherTool"""
    global _weather_tool
    if _weather_tool is None:
        _weather_tool = WeatherTool()
        logger.info("WeatherTool inicializado para agente IA")
    return _weather_tool


# ==============================================================================
# FUNÇÕES PRINCIPAIS - O que o agente vai chamar
# ==============================================================================

def get_weather(city: str) -> Dict[str, Any]:
    """
    Busca clima de uma cidade - FUNÇÃO PRINCIPAL para agentes
    
    Args:
        city: Nome da cidade (ex: "São Paulo", "New York")
        
    Returns:
        Dict com dados estruturados:
        {
            "success": True/False,
            "city": "São Paulo",
            "country": "BR",
            "temperature": 25.5,
            "feels_like": 26.0,
            "conditions": "céu limpo",
            "humidity": 60,
            "wind_speed": 3.5,
            "message": "Descrição legível para humanos"
        }
        
    Exemplo:
        >>> get_weather("São Paulo")
        {'success': True, 'city': 'São Paulo', 'temperature': 25.5, ...}
    """
    tool = _get_tool()
    
    try:
        # Busca dados
        data = tool.get_weather_for_agent(city)
        
        # Extrai campos importantes
        temp = data["temperature"]["current"]
        feels = data["temperature"]["feels_like"]
        conditions = data["conditions"]
        humidity = data["humidity"]
        wind = data["current_weather"]["wind"]["speed"]
        
        # Cria mensagem legível
        message = (
            f"Em {data['location']['city']}, {data['location']['country']}: "
            f"{temp}°C (sensação de {feels}°C), {conditions}, "
            f"umidade {humidity}%, vento {wind} m/s"
        )
        
        # Retorna formato simplificado
        return {
            "success": True,
            "city": data["location"]["city"],
            "country": data["location"]["country"],
            "temperature": temp,
            "feels_like": feels,
            "conditions": conditions,
            "humidity": humidity,
            "wind_speed": wind,
            "message": message
        }
        
    except CityNotFoundError:
        logger.warning(f"Cidade não encontrada: {city}")
        return {
            "success": False,
            "error": "city_not_found",
            "message": f"Cidade '{city}' não encontrada"
        }
    
    except WeatherAPIError as e:
        logger.error(f"Erro na API: {e}")
        return {
            "success": False,
            "error": "api_error",
            "message": str(e)
        }
    
    except Exception as e:
        logger.exception(f"Erro inesperado: {e}")
        return {
            "success": False,
            "error": "unknown",
            "message": f"Erro inesperado: {str(e)}"
        }


def is_beach_weather(city: str, min_temp: float = 25.0) -> Dict[str, Any]:
    """
    Verifica se está bom para praia
    
    Args:
        city: Nome da cidade
        min_temp: Temperatura mínima para considerar "bom para praia" (padrão: 25°C)
        
    Returns:
        Dict com análise:
        {
            "success": True,
            "good_for_beach": True/False,
            "temperature": 28.5,
            "conditions": "céu limpo",
            "recommendation": "Perfeito para praia!"
        }
    """
    result = get_weather(city)
    
    if not result["success"]:
        return result
    
    temp = result["temperature"]
    conditions = result["conditions"].lower()
    
    # Verifica condições
    good_temp = temp >= min_temp
    no_rain = "chuva" not in conditions and "rain" not in conditions
    
    good_for_beach = good_temp and no_rain
    
    # Gera recomendação
    if good_for_beach:
        recommendation = f"Perfeito para praia! {temp}°C e {result['conditions']}"
    elif not good_temp:
        recommendation = f"Muito frio para praia ({temp}°C)"
    elif not no_rain:
        recommendation = f"Não recomendado: {result['conditions']}"
    else:
        recommendation = "Condições não ideais para praia"
    
    return {
        "success": True,
        "city": result["city"],
        "good_for_beach": good_for_beach,
        "temperature": temp,
        "conditions": result["conditions"],
        "recommendation": recommendation
    }


def compare_weather(cities: List[str]) -> Dict[str, Any]:
    """
    Compara clima de múltiplas cidades
    
    Args:
        cities: Lista de nomes de cidades
        
    Returns:
        Dict com comparação:
        {
            "success": True,
            "cities": [...],
            "hottest": {"city": "Rio", "temp": 32.0},
            "coldest": {"city": "Curitiba", "temp": 18.0},
            "summary": "Texto resumindo a comparação"
        }
    """
    results = []
    errors = []
    
    for city in cities:
        data = get_weather(city)
        if data["success"]:
            results.append(data)
        else:
            errors.append(city)
    
    if not results:
        return {
            "success": False,
            "error": "no_data",
            "message": "Não foi possível obter dados de nenhuma cidade"
        }
    
    # Encontra extremos
    hottest = max(results, key=lambda x: x["temperature"])
    coldest = min(results, key=lambda x: x["temperature"])
    
    # Cria resumo
    summary_lines = []
    for r in results:
        summary_lines.append(
            f"- {r['city']}: {r['temperature']}°C, {r['conditions']}"
        )
    
    summary = "\n".join(summary_lines)
    summary += f"\n\nMais quente: {hottest['city']} ({hottest['temperature']}°C)"
    summary += f"\nMais fria: {coldest['city']} ({coldest['temperature']}°C)"
    
    return {
        "success": True,
        "cities": results,
        "hottest": {
            "city": hottest["city"],
            "temperature": hottest["temperature"]
        },
        "coldest": {
            "city": coldest["city"],
            "temperature": coldest["temperature"]
        },
        "errors": errors if errors else None,
        "summary": summary
    }


# ==============================================================================
# TESTE - Executa se rodar direto: python weather_for_agents.py
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TESTE: Interface para Agentes IA")
    print("=" * 70)
    
    # Teste 1: Busca simples
    print("\n1. Busca clima de São Paulo:")
    result = get_weather("São Paulo")
    print(result)
    
    # Teste 2: Verifica se dá praia
    print("\n2. Verifica se está bom para praia no Rio:")
    beach = is_beach_weather("Rio de Janeiro")
    print(beach)
    
    # Teste 3: Compara cidades
    print("\n3. Compara 3 cidades:")
    comparison = compare_weather(["São Paulo", "Rio de Janeiro", "Curitiba"])
    print(comparison["summary"])
    
    # Teste 4: Erro (cidade inexistente)
    print("\n4. Teste de erro (cidade inexistente):")
    error = get_weather("CidadeQueNaoExiste123")
    print(error)
    
    print("\n" + "=" * 70)
    print("Testes concluídos!")