# Guia Simples de OOP - WeatherClient

Este guia explica os conceitos básicos de Orientação a Objetos (OOP) usando o exemplo do `WeatherClient`.

## 🎯 **O que é OOP?**

OOP é uma forma de organizar código agrupando **dados** (atributos) e **comportamentos** (métodos) em **classes**.

### **Antes (Código Procedural)**
```python
# Função simples - sem estado
def fetch_weather_data(city: str, api_key: str) -> dict:
    # Sempre faz nova requisição
    # Não lembra de consultas anteriores
    response = requests.get(url, params={"q": city, "appid": api_key})
    return response.json()
```

### **Depois (Código OOP)**
```python
# Classe com estado
class WeatherClient:
    def __init__(self):
        self._cache = {}  # Estado: lembra dados anteriores
    
    def get_weather(self, city: str):
        # Verifica cache primeiro
        if city in self._cache:
            return self._cache[city]  # Reutiliza dados
        
        # Só faz nova requisição se necessário
        data = self._make_request(city)
        self._cache[city] = data  # Salva para próxima vez
        return data
```

## 🏗️ **Conceitos Básicos**

### 1. **Classe**
Uma "receita" que define como criar objetos:

```python
class WeatherClient:
    """Cliente para API do clima"""
    
    def __init__(self):
        """Construtor - inicializa o objeto"""
        self._config = get_settings()
        self._cache = {}
    
    def get_weather(self, city: str):
        """Método - comportamento do objeto"""
        # Lógica aqui
        pass
```

### 2. **Atributos (Dados)**
Variáveis que pertencem ao objeto:

```python
class WeatherClient:
    def __init__(self):
        # Atributos públicos
        self.name = "WeatherClient"
        
        # Atributos privados (convenção: _ no início)
        self._config = get_settings()
        self._cache = {}
```

### 3. **Métodos (Comportamentos)**
Funções que pertencem ao objeto:

```python
class WeatherClient:
    def get_weather(self, city: str):
        """Método público"""
        return self._check_cache(city)
    
    def _check_cache(self, city: str):
        """Método privado (convenção: _ no início)"""
        return self._cache.get(city)
```

### 4. **Estado**
Informações que o objeto "lembra" entre chamadas:

```python
# Criar cliente
client = WeatherClient()

# Primeira consulta - vai para API
weather1 = client.get_weather("São Paulo")

# Segunda consulta - usa cache (estado!)
weather2 = client.get_weather("São Paulo")  # Mais rápido!
```

## 🔄 **Vantagens do Estado**

### **Sem Estado (Procedural)**
```python
# Cada chamada é independente
data1 = fetch_weather_data("São Paulo", api_key)  # Requisição HTTP
data2 = fetch_weather_data("São Paulo", api_key)  # Outra requisição HTTP
data3 = fetch_weather_data("São Paulo", api_key)  # Mais uma requisição HTTP
```

### **Com Estado (OOP)**
```python
client = WeatherClient()

# Primeira chamada - vai para API
data1 = client.get_weather("São Paulo")  # Requisição HTTP

# Chamadas seguintes - usa cache
data2 = client.get_weather("São Paulo")  # Cache hit!
data3 = client.get_weather("São Paulo")  # Cache hit!
```

## 📊 **Exemplo Prático**

### **Código Simplificado do WeatherClient**

```python
class WeatherData:
    """Modelo para dados climáticos"""
    def __init__(self, city_name, temperature, description):
        self.city_name = city_name
        self.temperature = temperature
        self.description = description
    
    def get_summary(self):
        """Método útil para resumo"""
        return f"{self.city_name}: {self.temperature}°C, {self.description}"

class WeatherClient:
    """Cliente com estado (cache)"""
    
    def __init__(self):
        # Estado da classe
        self._config = get_settings()
        self._cache = {}  # {cidade: dados}
    
    def get_weather(self, city: str) -> WeatherData:
        # Verificar cache (estado!)
        if city in self._cache:
            cache_time = self._cache[city]['timestamp']
            if datetime.now() - cache_time < timedelta(minutes=10):
                return self._cache[city]['data']
        
        # Fazer requisição
        data = self._make_request(city)
        weather = WeatherData(
            city_name=data['name'],
            temperature=data['main']['temp'],
            description=data['weather'][0]['description']
        )
        
        # Salvar no cache (estado!)
        self._cache[city] = {
            'data': weather,
            'timestamp': datetime.now()
        }
        
        return weather
    
    def get_cache_info(self):
        """Método para verificar estado"""
        return {
            'cities_cached': list(self._cache.keys()),
            'cache_size': len(self._cache)
        }
```

### **Como Usar**

```python
# Criar cliente
client = WeatherClient()

# Primeira consulta
weather = client.get_weather("São Paulo")
print(weather.get_summary())  # São Paulo: 25°C, nublado

# Segunda consulta (usa cache)
weather2 = client.get_weather("São Paulo")  # Mais rápido!

# Ver estado do cache
info = client.get_cache_info()
print(f"Cidades em cache: {info['cities_cached']}")
```

## 🎓 **Conceitos Importantes**

### **Encapsulamento**
- **Atributos privados** (`_cache`, `_config`) - não devem ser acessados diretamente
- **Métodos públicos** (`get_weather()`) - interface da classe

### **Estado vs Funções**
- **Função**: Sempre faz a mesma coisa, não "lembra" nada
- **Classe**: Mantém informações entre chamadas (cache, configurações, etc.)

### **Reutilização**
- **Função**: Cada chamada é independente
- **Classe**: Pode reutilizar dados e configurações

## 🚀 **Quando Usar OOP?**

### **Use OOP quando:**
- Precisa manter estado entre operações (cache, configurações)
- Tem dados relacionados que fazem sentido juntos
- Quer encapsular lógica complexa
- Precisa reutilizar configurações ou conexões

### **Use funções quando:**
- Operação é simples e independente
- Não precisa manter estado
- Lógica é puramente matemática/transformação

## 📝 **Resumo**

OOP permite criar objetos que:
1. **Encapsulam** dados e comportamentos
2. **Mantêm estado** entre operações
3. **Reutilizam** configurações e dados
4. **Organizam** código de forma lógica

No `WeatherClient`:
- **Estado**: Cache de consultas anteriores
- **Comportamento**: Métodos para consultar clima
- **Vantagem**: Evita requisições desnecessárias à API

```python
# Simples e eficiente
client = WeatherClient()
weather = client.get_weather("São Paulo")  # Pode usar cache!
```
