# Weather Tool

Ferramenta de consulta de clima otimizada para agentes IA, construída com Python e orientação a objetos.

## Sobre o Projeto

Este é um **pacote Python** que consulta dados climáticos da API OpenWeatherMap, com:
- Cache inteligente (10 minutos)
- Validação automática de dados (Pydantic)
- Tratamento robusto de erros
- Interface otimizada para agentes IA

### Estrutura do Projeto

```
weather_api_tool/
├── weather_tool/              # Pacote principal (biblioteca)
│   ├── __init__.py            # Expõe API pública
│   ├── client.py              # Lógica principal + cache
│   ├── models.py              # Modelos de dados (Pydantic)
│   ├── settings.py            # Configurações
│   └── exceptions.py          # Erros customizados
│
├── examples/                  # Exemplos de uso
│   ├── basic_usage.py         # Uso básico
│   ├── cli_weather.py         # CLI interativo
│   └── weather_for_agents.py  # Interface para agentes IA
│
├── tests/                     # Testes automatizados
│   └── test_basic.py
│
├── .env                       # Configurações (API key)
├── pyproject.toml             # Dependências
└── README.md                  # Este arquivo
```

## Instalação

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd weather_api_tool
```

### 2. Crie ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instale dependências
```bash
pip install -e .
```

### 4. Configure a API key

Crie arquivo `.env` na raiz:
```env
OPENWEATHER_API_KEY=sua_chave_aqui
```

Obtenha sua chave em: https://openweathermap.org/api

## Uso

### Uso Básico (Python)

```python
from weather_tool import WeatherTool

# Cria instância
tool = WeatherTool()

# Busca clima
weather = tool.get_weather("São Paulo")

# Exibe formatado
print(weather.to_display_format())
```

### CLI Interativo

```bash
python examples/cli_weather.py
```

Interface interativa para consultar clima de qualquer cidade.

### Para Agentes IA

```python
from examples.weather_for_agents import get_weather, is_beach_weather

# Busca clima
result = get_weather("Rio de Janeiro")
# Retorna: {"success": True, "temperature": 28.5, ...}

# Verifica se dá praia
beach = is_beach_weather("Salvador")
# Retorna: {"good_for_beach": True, "recommendation": "Perfeito para praia!"}
```

## API do Pacote

### `WeatherTool`

Classe principal com métodos:

#### `get_weather(city: str) -> WeatherData`
Busca dados climáticos com cache automático.

```python
tool = WeatherTool()
weather = tool.get_weather("Brasília")
```

#### `get_weather_for_agent(city: str) -> dict`
Retorna dados em formato JSON otimizado para IA.

```python
data = tool.get_weather_for_agent("Curitiba")
# Retorna dict estruturado
```

#### `display_weather(city: str) -> str`
Retorna string formatada para exibição.

```python
formatted = tool.display_weather("Fortaleza")
print(formatted)
```

#### `get_cache_info() -> dict`
Informações sobre o cache atual.

```python
info = tool.get_cache_info()
# {'total_cities': 3, 'valid_entries': 2, ...}
```

#### `clear_cache() -> None`
Limpa todo o cache.

```python
tool.clear_cache()
```

## Interface para Agentes IA

O arquivo `examples/weather_for_agents.py` contém funções prontas para agentes:

### `get_weather(city: str) -> dict`
Busca clima e retorna dict estruturado.

### `is_beach_weather(city: str, min_temp: float = 25.0) -> dict`
Analisa se está bom para praia.

### `compare_weather(cities: List[str]) -> dict`
Compara clima de múltiplas cidades.

**Exemplo de uso pelo agente:**
```python
from examples.weather_for_agents import is_beach_weather

# Usuário pergunta: "Dá praia no Rio hoje?"
result = is_beach_weather("Rio de Janeiro")

if result["good_for_beach"]:
    print(result["recommendation"])
    # "Perfeito para praia! 28.5°C e céu limpo"
```

## Arquitetura OOP

### Separação de Responsabilidades

| Arquivo | Responsabilidade |
|---------|------------------|
| `settings.py` | Configuração e validação |
| `exceptions.py` | Erros customizados |
| `models.py` | Estrutura de dados e validação |
| `client.py` | Lógica de negócio e cache |

### Fluxo de Dados

```
Usuário
  ↓
examples/weather_for_agents.py (orquestrador)
  ↓
weather_tool.client.WeatherTool (lógica)
  ├─ Verifica cache
  ├─ Faz request HTTP (se necessário)
  ├─ Valida com Pydantic (models.py)
  └─ Retorna WeatherData
  ↓
Formata para agente IA
  ↓
Retorna dict/JSON
```

### Cache Inteligente

- Duração: 10 minutos
- Baseado em timestamp
- Evita requisições desnecessárias
- Transparente para o usuário

## Tratamento de Erros

O pacote define erros específicos:

```python
from weather_tool import CityNotFoundError, WeatherAPIError

try:
    weather = tool.get_weather("XYZ123")
except CityNotFoundError:
    print("Cidade não encontrada")
except WeatherAPIError as e:
    print(f"Erro na API: {e}")
```

## Testes

Execute os testes:
```bash
pytest tests/
```

## Logs

O pacote usa `loguru` para logging:
- INFO: Operações principais
- DEBUG: Detalhes técnicos
- WARNING: Problemas não-fatais
- ERROR: Erros recuperáveis

Logs são salvos em `logs/` (se configurado).

## Dependências

- `requests` - Requisições HTTP
- `pydantic` - Validação de dados
- `pydantic-settings` - Configurações
- `loguru` - Logging
- `python-dotenv` - Variáveis de ambiente

## Limitações

- API gratuita: 60 chamadas/minuto
- Apenas clima atual (não previsão)
- Cache em memória (não persiste entre execuções)

## Próximos Passos

- [ ] Adicionar previsão de 5 dias
- [ ] Cache persistente (Redis/arquivo)
- [ ] Suporte async para múltiplas cidades
- [ ] Retry automático em falhas de rede

## Licença

MIT License

## Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Autor

Fábio Lima - Estudante de Python OOP