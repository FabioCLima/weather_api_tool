#!/usr/bin/env python3
"""
Exemplo simples do WeatherClient com OOP.

Este exemplo demonstra conceitos básicos de OOP:
1. Classe com estado (cache)
2. Métodos que operam no estado
3. Encapsulamento (atributos privados)
4. Validação simples com Pydantic
"""

import sys
from pathlib import Path

# Adicionar o src ao path para permitir importações absolutas
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importações absolutas - mais limpas e profissionais
from weather_tool import WeatherClient, WeatherData, get_settings, ConfigurationError
from weather_tool.client import fetch_weather_data


def exemplo_basico():
    """Exemplo básico de uso do WeatherClient."""
    print("🌤️  Exemplo Básico - WeatherClient")
    print("=" * 40)
    
    try:
        # Criar cliente (carrega configuração automaticamente)
        client = WeatherClient()
        
        # Obter clima para uma cidade
        weather = client.get_weather("São Paulo")
        
        print(f"Cidade: {weather.city_name}")
        print(f"Temperatura: {weather.temperature}°C")
        print(f"Descrição: {weather.description}")
        print(f"Umidade: {weather.humidity}%")
        print(f"Vento: {weather.wind_speed} m/s")
        
        # Usar método da classe
        print(f"Resumo: {weather.get_summary()}")
        
    except ConfigurationError as e:
        print(f"❌ Erro de configuração: {e}")
        print("💡 Configure OPENWEATHER_API_KEY no .env")
    except Exception as e:
        print(f"❌ Erro: {e}")


def exemplo_com_cache():
    """Exemplo demonstrando o cache (estado da classe)."""
    print("\n🔄 Exemplo com Cache - Estado da Classe")
    print("=" * 40)
    
    try:
        client = WeatherClient()
        
        # Primeira consulta (vai para a API)
        print("1️⃣ Primeira consulta para São Paulo...")
        weather1 = client.get_weather("São Paulo")
        print(f"   Temperatura: {weather1.temperature}°C")
        
        # Segunda consulta (vai usar cache)
        print("2️⃣ Segunda consulta para São Paulo (cache)...")
        weather2 = client.get_weather("São Paulo")
        print(f"   Temperatura: {weather2.temperature}°C")
        
        # Mostrar informações do cache
        cache_info = client.get_cache_info()
        print(f"\n💾 Cache: {cache_info['cache_size']} cidades")
        print(f"   Cidades em cache: {cache_info['cities_cached']}")
        
        # Limpar cache
        client.clear_cache()
        print("   Cache limpo!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


def exemplo_multiplas_cidades():
    """Exemplo consultando múltiplas cidades."""
    print("\n🏙️  Exemplo - Múltiplas Cidades")
    print("=" * 40)
    
    try:
        client = WeatherClient()
        
        cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte"]
        
        print(f"Consultando {len(cidades)} cidades...")
        
        for cidade in cidades:
            try:
                weather = client.get_weather(cidade)
                print(f"   🌤️  {weather.get_summary()}")
            except Exception as e:
                print(f"   ❌ {cidade}: Erro - {e}")
        
        # Mostrar cache final
        cache_info = client.get_cache_info()
        print(f"\n💾 Total em cache: {cache_info['cache_size']} cidades")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


def exemplo_comparacao():
    """Comparação entre OOP e função procedural."""
    print("\n🔄 Comparação - OOP vs Procedural")
    print("=" * 40)
    
    try:
        cidade = "São Paulo"
        settings = get_settings()
        
        # Nova implementação (OOP)
        print("1️⃣ Nova implementação (OOP):")
        client = WeatherClient()
        weather_oop = client.get_weather(cidade)
        print(f"   {weather_oop.get_summary()}")
        print(f"   Tipo: {type(weather_oop)}")
        
        # Função legada (procedural)
        print("\n2️⃣ Função legada (procedural):")
        weather_legacy = fetch_weather_data(cidade, settings.api_key)
        print(f"   {weather_legacy['name']}: {weather_legacy['main']['temp']}°C")
        print(f"   Tipo: {type(weather_legacy)}")
        
        print("\n💡 Vantagens da versão OOP:")
        print("   ✅ Estado encapsulado (cache)")
        print("   ✅ Validação automática")
        print("   ✅ Métodos úteis (get_summary())")
        print("   ✅ Reutilização da instância")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


def main():
    """Função principal."""
    print("🚀 Exemplos Simples - WeatherClient com OOP")
    print("=" * 50)
    
    # Verificar configuração
    try:
        settings = get_settings()
        api_key_masked = f"{settings.api_key[:8]}...{settings.api_key[-4:]}"
        print(f"🔑 API Key: {api_key_masked}")
    except ConfigurationError:
        print("⚠️  Configure OPENWEATHER_API_KEY no .env")
        return
    
    # Executar exemplos
    exemplo_basico()
    exemplo_com_cache()
    exemplo_multiplas_cidades()
    exemplo_comparacao()
    
    print("\n🎉 Exemplos concluídos!")
    print("\n📚 Conceitos básicos de OOP demonstrados:")
    print("   1. Classe: Encapsula dados e comportamentos")
    print("   2. Estado: Atributos mantêm informações (_cache)")
    print("   3. Métodos: Operações que usam o estado")
    print("   4. Encapsulamento: Atributos privados (_cache)")
    print("   5. Validação: Pydantic para dados consistentes")


if __name__ == "__main__":
    main()
