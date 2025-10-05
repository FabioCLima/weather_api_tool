# examples/cli_weather.py ← ORQUESTRADOR #2
"""CLI interativo para consultar clima"""
import sys
from weather_tool import WeatherTool, CityNotFoundError
from loguru import logger

def main():
    """Orquestra interação com usuário"""
    tool = WeatherTool()
    
    print("🌤️  Weather Tool CLI")
    print("=" * 50)
    
    # Loop de interação
    while True:
        try:
            # 1. Recebe entrada
            city = input("\n🏙️  Digite a cidade (ou 'q' para sair): ").strip()
            
            if city.lower() in ['q', 'quit', 'sair']:
                print("👋 Até logo!")
                break
            
            # 2. Usa o pacote
            weather = tool.get_weather(city)
            
            # 3. Exibe resultado
            print(weather.to_display_format())
            
            # 4. Mostra cache
            cache_info = tool.get_cache_info()
            print(f"\n📊 Cidades no cache: {cache_info['valid_entries']}")
            
        except CityNotFoundError as e:
            print(f"❌ {e}")
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break

if __name__ == "__main__":
    main()