#!/usr/bin/env python3
"""
Exemplo de uso da Weather Tool refatorada - Migração de Procedural para OOP

Este exemplo demonstra como usar a nova versão OOP da Weather Tool
e compara com o código procedural antigo.
"""

from weather_tool import WeatherTool, WeatherAPIError, get_settings
import json
from loguru import logger


def exemplo_codigo_procedural_antigo():
    """
    Como era feito ANTES (código procedural):
    
    # Funções separadas, sem estado, sem cache
    api_key = load_api_key(".env")
    city = get_city_from_user()
    data = fetch_weather_data(city, api_key)
    display_weather_data(data)
    """
    logger.info("=== CÓDIGO PROCEDURAL ANTIGO ===")
    logger.info("1. load_api_key() - carregava chave do .env")
    logger.info("2. get_city_from_user() - pedia cidade ao usuário")
    logger.info("3. fetch_weather_data() - fazia requisição HTTP")
    logger.info("4. display_weather_data() - mostrava dados")
    logger.info("❌ Sem cache, sem validação, sem estado")
    logger.info("❌ Cada chamada = nova requisição HTTP")


def exemplo_codigo_oop_novo():
    """
    Como é feito AGORA (código OOP):
    
    # Uma classe com estado, cache, validação
    tool = WeatherTool()
    weather_data = tool.get_weather(city)
    """
    logger.info("\n=== CÓDIGO OOP NOVO ===")
    
    try:
        # 1. Inicializar a ferramenta (carrega config automaticamente)
        tool = WeatherTool()
        logger.success("✅ WeatherTool inicializada com configuração")
        
        # 2. Buscar dados do clima (com cache automático)
        city = "São Paulo"
        logger.info(f"Buscando clima para: {city}")
        
        # Método principal - retorna objeto WeatherData
        weather_data = tool.get_weather(city)
        logger.success("✅ Dados obtidos e validados com Pydantic")
        
        # 3. Exibir dados formatados
        print(weather_data.to_display_format())
        
        # 4. Obter dados em formato JSON para agentes IA
        json_data = weather_data.to_agent_format()
        logger.info("📊 Dados em formato JSON para IA:")
        logger.info(json.dumps(json_data, indent=2, ensure_ascii=False))
        
        # 5. Verificar cache
        cache_info = tool.get_cache_info()
        logger.info(f"💾 Cache: {cache_info}")
        
        # 6. Segunda consulta (usa cache!)
        logger.info("\n🔄 Segunda consulta (deve usar cache):")
        weather_data2 = tool.get_weather(city)
        logger.info("✅ Usou cache - sem nova requisição HTTP!")
        
        return weather_data
        
    except WeatherAPIError as e:
        logger.error(f"Erro da API: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")


def exemplo_para_agentes_ia():
    """Exemplo específico para uso com agentes IA"""
    logger.info("\n=== EXEMPLO PARA AGENTES IA ===")
    
    try:
        tool = WeatherTool()
        
        # Método otimizado para agentes IA
        json_weather = tool.get_weather_json("Rio de Janeiro")
        
        logger.info("🤖 Dados otimizados para agentes IA:")
        print(json.dumps(json_weather, indent=2, ensure_ascii=False))
        
        # Informações específicas que agentes IA podem usar
        location = json_weather["location"]
        current = json_weather["current_weather"]
        
        logger.info(f"📍 Local: {location['city']}, {location['country']}")
        logger.info(f"🌡 Temperatura: {current['temperature']['current']}°C")
        logger.info(f"🌤 Condições: {current['conditions']['description']}")
        logger.info(f"💧 Umidade: {current['humidity']}%")
        
    except Exception as e:
        logger.error(f"Erro: {e}")


def comparacao_vantagens():
    """Demonstra as vantagens do código OOP"""
    logger.info("\n=== VANTAGENS DO CÓDIGO OOP ===")
    
    advantages = [
        "✅ Cache inteligente - evita requisições desnecessárias",
        "✅ Validação automática com Pydantic",
        "✅ Tratamento de erros centralizado",
        "✅ Estado mantido entre operações",
        "✅ Múltiplos formatos de saída (JSON, display, simples)",
        "✅ Configuração centralizada",
        "✅ Logs detalhados para debugging",
        "✅ Compatibilidade com código legado",
        "✅ Fácil extensão e manutenção"
    ]
    
    for advantage in advantages:
        logger.info(advantage)


def main():
    """Função principal demonstrando a migração"""
    logger.info("🚀 DEMONSTRAÇÃO: Migração de Procedural para OOP")
    logger.info("=" * 60)
    
    # Mostrar como era antes
    exemplo_codigo_procedural_antigo()
    
    # Mostrar como é agora
    weather_data = exemplo_codigo_oop_novo()
    
    # Exemplo para agentes IA
    exemplo_para_agentes_ia()
    
    # Vantagens
    comparacao_vantagens()
    
    logger.success("\n🎉 Migração concluída com sucesso!")
    logger.info("Agora você tem uma ferramenta robusta e orientada a objetos!")


if __name__ == "__main__":
    main()
