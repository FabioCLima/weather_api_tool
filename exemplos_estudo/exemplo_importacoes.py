#!/usr/bin/env python3
"""
Exemplos de importações absolutas vs relativas.

Este arquivo demonstra as diferentes formas de importar módulos
e as vantagens das importações absolutas.
"""

import sys
from pathlib import Path

# Adicionar src ao path para permitir importações absolutas
sys.path.insert(0, str(Path(__file__).parent / "src"))


def exemplo_importacoes_absolutas():
    """Demonstra importações absolutas - RECOMENDADO."""
    print("🎯 Importações Absolutas (RECOMENDADO)")
    print("=" * 50)
    
    # Forma 1: Importar do pacote principal
    from weather_tool import WeatherClient, WeatherData, get_settings
    print("✅ from weather_tool import WeatherClient, WeatherData, get_settings")
    
    # Forma 2: Importar módulos específicos
    from weather_tool.client import WeatherClient
    from weather_tool.settings import WeatherAPIConfig
    print("✅ from weather_tool.client import WeatherClient")
    print("✅ from weather_tool.settings import WeatherAPIConfig")
    
    # Forma 3: Importar tudo do pacote
    import weather_tool
    print("✅ import weather_tool")
    print(f"   Versão: {weather_tool.__version__}")
    
    print("\n💡 Vantagens das importações absolutas:")
    print("   ✅ Mais claras e explícitas")
    print("   ✅ Funcionam de qualquer lugar")
    print("   ✅ Mais fáceis de refatorar")
    print("   ✅ Melhor para IDEs e ferramentas")


def exemplo_importacoes_relativas():
    """Demonstra importações relativas - NÃO RECOMENDADO para uso externo."""
    print("\n⚠️  Importações Relativas (dentro do pacote)")
    print("=" * 50)
    
    # Importações relativas só funcionam dentro do próprio pacote
    print("# Dentro de weather_tool/client.py:")
    print("from .settings import get_settings  # Relativa")
    print("from ..other_module import something  # Relativa")
    
    print("\n❌ Problemas das importações relativas:")
    print("   ❌ Confusas e difíceis de seguir")
    print("   ❌ Não funcionam fora do pacote")
    print("   ❌ Difíceis de testar")
    print("   ❌ Problemas com refatoração")


def exemplo_uso_pratico():
    """Exemplo prático de uso com importações absolutas."""
    print("\n🚀 Exemplo Prático - Uso das Importações")
    print("=" * 50)
    
    try:
        # Importação limpa e clara
        from weather_tool import WeatherClient, get_settings
        
        print("1️⃣ Criando cliente:")
        client = WeatherClient()
        
        print("2️⃣ Verificando configuração:")
        settings = get_settings()
        print(f"   API Key configurada: {settings.api_key[:8]}...")
        
        print("3️⃣ Consultando clima:")
        weather = client.get_weather("São Paulo")
        print(f"   {weather.get_summary()}")
        
        print("\n✅ Importações absolutas funcionando perfeitamente!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


def exemplo_comparacao():
    """Comparação entre diferentes estilos de importação."""
    print("\n📊 Comparação de Estilos de Importação")
    print("=" * 50)
    
    print("🔴 CÓDIGO PROCEDURAL (antigo):")
    print("""
    import sys
    sys.path.append('src')
    from weather_tool.client import fetch_weather_data
    from weather_tool.settings import load_api_key
    
    api_key = load_api_key('.env')
    data = fetch_weather_data('São Paulo', api_key)
    """)
    
    print("🟡 CÓDIGO OOP COM IMPORTAÇÕES RELATIVAS:")
    print("""
    from .settings import get_settings
    
    class WeatherClient:
        def __init__(self):
            self._config = get_settings()
    """)
    
    print("🟢 CÓDIGO OOP COM IMPORTAÇÕES ABSOLUTAS (RECOMENDADO):")
    print("""
    from weather_tool.settings import get_settings
    # ou melhor ainda:
    from weather_tool import WeatherClient, get_settings
    
    client = WeatherClient()
    weather = client.get_weather('São Paulo')
    """)


def exemplo_instalacao_pacote():
    """Mostra como o pacote seria usado após instalação."""
    print("\n📦 Como Usar Após Instalação do Pacote")
    print("=" * 50)
    
    print("1️⃣ Instalar o pacote:")
    print("   pip install -e .  # Instalação em modo desenvolvimento")
    print("   # ou")
    print("   pip install .     # Instalação normal")
    
    print("\n2️⃣ Usar em qualquer lugar:")
    print("""
    # Em qualquer arquivo Python
    from weather_tool import WeatherClient
    
    client = WeatherClient()
    weather = client.get_weather("São Paulo")
    print(weather.get_summary())
    """)
    
    print("3️⃣ Sem precisar mexer no sys.path!")
    print("   ✅ Funciona de qualquer diretório")
    print("   ✅ Importações sempre funcionam")
    print("   ✅ Código mais profissional")


def main():
    """Função principal."""
    print("📚 Guia de Importações Absolutas vs Relativas")
    print("=" * 60)
    
    exemplo_importacoes_absolutas()
    exemplo_importacoes_relativas()
    exemplo_uso_pratico()
    exemplo_comparacao()
    exemplo_instalacao_pacote()
    
    print("\n🎉 Resumo:")
    print("   ✅ Use importações absolutas sempre que possível")
    print("   ✅ Configure o __init__.py para facilitar imports")
    print("   ✅ Use 'pip install -e .' para desenvolvimento")
    print("   ✅ Evite mexer no sys.path em código de produção")


if __name__ == "__main__":
    main()
