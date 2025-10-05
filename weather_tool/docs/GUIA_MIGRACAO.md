# 🚀 Guia de Migração: Procedural → OOP

Este guia te ajuda a entender como migrar do código procedural para orientação a objetos na Weather Tool.

## 📊 Comparação: Antes vs Depois

### **ANTES (Código Procedural)**

```python
# Funções separadas, sem estado
def load_api_key(env_file: str) -> Optional[str]:
    # Carrega chave do .env
    
def get_city_from_user() -> str:
    # Pede cidade ao usuário
    
def fetch_weather_data(city: str, api_key: str) -> Dict[str, Any]:
    # Faz requisição HTTP
    
def display_weather_data(data: Optional[Dict[str, Any]]) -> None:
    # Exibe dados

# Uso:
api_key = load_api_key(".env")
city = get_city_from_user()
data = fetch_weather_data(city, api_key)
display_weather_data(data)
```

### **DEPOIS (Código OOP)**

```python
# Uma classe com estado, cache, validação
class WeatherTool:
    def __init__(self):
        self._cache = {}  # Estado!
        self.config = get_settings()
    
    def get_weather(self, city: str) -> WeatherData:
        # Busca com cache automático
        
    def get_weather_json(self, city: str) -> Dict[str, Any]:
        # Formato otimizado para IA
        
    def display_weather(self, city: str) -> str:
        # Exibição formatada

# Uso:
tool = WeatherTool()
weather_data = tool.get_weather(city)
```

## 🔄 Mapeamento de Funções

| **Função Antiga** | **Método Novo** | **Vantagem** |
|------------------|-----------------|--------------|
| `load_api_key()` | `WeatherTool.__init__()` | Configuração automática |
| `get_city_from_user()` | Parâmetro do método | Flexibilidade |
| `fetch_weather_data()` | `get_weather()` | Com cache e validação |
| `display_weather_data()` | `to_display_format()` | Integrado ao modelo |

## 🎯 Principais Melhorias

### 1. **Cache Inteligente**
```python
# ANTES: Cada chamada = nova requisição HTTP
data1 = fetch_weather_data("São Paulo", api_key)  # HTTP
data2 = fetch_weather_data("São Paulo", api_key)  # HTTP novamente!

# DEPOIS: Cache automático
tool = WeatherTool()
data1 = tool.get_weather("São Paulo")  # HTTP
data2 = tool.get_weather("São Paulo")  # Cache hit!
```

### 2. **Validação com Pydantic**
```python
# ANTES: Sem validação
data = response.json()  # Pode ter qualquer estrutura

# DEPOIS: Validação automática
weather_data = WeatherData.parse_obj(data)  # Validação completa
```

### 3. **Múltiplos Formatos de Saída**
```python
weather_data = tool.get_weather("São Paulo")

# Para exibição
print(weather_data.to_display_format())

# Para agentes IA
json_data = weather_data.to_agent_format()

# Para código legado
simple_data = weather_data.to_simple_dict()
```

### 4. **Tratamento de Erros Centralizado**
```python
# ANTES: Erros em cada função
try:
    api_key = load_api_key(".env")
    if not api_key:
        raise ValueError("API key not found")
    # ... mais validações
except Exception as e:
    # Tratamento disperso

# DEPOIS: Exceção personalizada
try:
    weather_data = tool.get_weather(city)
except WeatherAPIError as e:
    logger.error(f"Erro da API: {e}")
```

## 🛠️ Como Migrar Seu Código

### **Passo 1: Substituir Inicialização**
```python
# ANTES
api_key = load_api_key(".env")
if not api_key:
    raise ValueError("API key not found")

# DEPOIS
tool = WeatherTool()  # Configuração automática
```

### **Passo 2: Substituir Busca de Dados**
```python
# ANTES
data = fetch_weather_data(city, api_key)
if not data:
    logger.warning("No weather data")

# DEPOIS
try:
    weather_data = tool.get_weather(city)
    # Dados já validados e estruturados
except WeatherAPIError as e:
    logger.error(f"Erro: {e}")
```

### **Passo 3: Substituir Exibição**
```python
# ANTES
display_weather_data(data)

# DEPOIS
print(weather_data.to_display_format())
# OU
print(tool.display_weather(city))
```

### **Passo 4: Para Agentes IA**
```python
# ANTES: Dados brutos da API
data = fetch_weather_data(city, api_key)
# Precisa processar manualmente

# DEPOIS: JSON otimizado
json_data = tool.get_weather_json(city)
# Pronto para usar com agentes IA
```

## 🎨 Exemplos Práticos

### **Exemplo 1: Uso Básico**
```python
from weather_tool import WeatherTool

# Inicializar
tool = WeatherTool()

# Buscar clima
weather = tool.get_weather("São Paulo")

# Exibir
print(weather.to_display_format())
```

### **Exemplo 2: Para Agentes IA**
```python
from weather_tool import WeatherTool
import json

tool = WeatherTool()

# Dados em formato JSON otimizado
weather_json = tool.get_weather_json("Rio de Janeiro")

# Usar com agente IA
agent_response = f"""
Temperatura em {weather_json['location']['city']}: 
{weather_json['current_weather']['temperature']['current']}°C
Condições: {weather_json['current_weather']['conditions']['description']}
"""
```

### **Exemplo 3: Cache Management**
```python
tool = WeatherTool()

# Primeira consulta - vai para API
weather1 = tool.get_weather("São Paulo")

# Segunda consulta - usa cache
weather2 = tool.get_weather("São Paulo")

# Verificar cache
cache_info = tool.get_cache_info()
print(f"Cidades em cache: {cache_info['cached_cities']}")

# Limpar cache se necessário
tool.clear_cache()
```

## 🚀 Benefícios da Migração

1. **Performance**: Cache reduz requisições HTTP
2. **Confiabilidade**: Validação automática com Pydantic
3. **Manutenibilidade**: Código organizado em classes
4. **Extensibilidade**: Fácil adicionar novos recursos
5. **Debugging**: Logs detalhados
6. **Compatibilidade**: Funciona com código legado
7. **IA Ready**: JSON otimizado para agentes

## 📝 Checklist de Migração

- [ ] Substituir `load_api_key()` por `WeatherTool()`
- [ ] Substituir `fetch_weather_data()` por `get_weather()`
- [ ] Substituir `display_weather_data()` por `to_display_format()`
- [ ] Adicionar tratamento de `WeatherAPIError`
- [ ] Usar `get_weather_json()` para agentes IA
- [ ] Aproveitar cache automático
- [ ] Testar com diferentes cidades
- [ ] Verificar logs para debugging

## 🎯 Próximos Passos

1. **Teste a nova implementação** com o arquivo `exemplo_uso.py`
2. **Migre gradualmente** seu código existente
3. **Aproveite as novas funcionalidades** (cache, validação, etc.)
4. **Integre com agentes IA** usando `get_weather_json()`
5. **Explore extensões** como previsão do tempo, histórico, etc.

---

**🎉 Parabéns!** Você migrou com sucesso de código procedural para orientação a objetos, ganhando todas as vantagens de um código moderno, robusto e pronto para agentes IA!
