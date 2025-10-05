# Configuration System Guide

This guide explains the refactored configuration system in `src/weather_tool/settings.py` and demonstrates enterprise-level Python development practices.

## Overview

The configuration system has been completely refactored using:
- **Pydantic** for data validation and type safety
- **Object-Oriented Design** with proper abstraction
- **Design Patterns** (Factory, Singleton, Abstract Factory)
- **Professional Error Handling** with custom exceptions
- **Comprehensive Logging** for debugging and monitoring

## Key Learning Points for Data Scientists

### 1. Object-Oriented Programming (OOP)

```python
# Before: Simple function
def load_api_key(env_file: str) -> Optional[str]:
    # Basic file loading logic
    pass

# After: Class-based configuration with methods
class WeatherAPIConfig(BaseSettings):
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION
    
    def get_request_config(self) -> Dict[str, Any]:
        return {"timeout": self.timeout, "max_retries": self.max_retries}
```

### 2. Data Validation with Pydantic

```python
@validator('api_key')
def validate_api_key(cls, v: str) -> str:
    if not v or not v.strip():
        raise ValueError("API key cannot be empty")
    if len(v) < 10:
        raise ValueError("API key appears to be too short")
    return v.strip()
```

### 3. Design Patterns in Practice

#### Factory Pattern
```python
def get_settings(env_file_path: Optional[Union[str, Path]] = None) -> WeatherAPIConfig:
    """Factory function that creates configuration instances."""
    config_manager = get_config_manager(env_file_path)
    return config_manager.get_config()
```

#### Abstract Factory Pattern
```python
class ConfigurationManager(ABC):
    @abstractmethod
    def get_config(self) -> WeatherAPIConfig:
        pass
```

#### Singleton Pattern
```python
# Global configuration manager instance
_config_manager: Optional[EnvironmentConfigurationManager] = None
```

### 4. Error Handling Best Practices

```python
class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

# Usage with proper error handling
try:
    settings = get_settings()
except ConfigurationError as e:
    logger.error(f"Configuration failed: {e}")
    raise
```

### 5. Environment Variable Management

The system supports multiple ways to load configuration:

1. **Environment Variables**: Direct system environment variables
2. **.env Files**: Local development configuration files
3. **Default Values**: Sensible defaults for all settings

## Usage Examples

### Basic Usage

```python
from weather_tool.settings import get_settings

# Load configuration
settings = get_settings()

# Access configuration values
api_key = settings.api_key
timeout = settings.timeout
base_url = settings.base_url
```

### Advanced Usage

```python
from weather_tool.settings import get_settings, ConfigurationError

try:
    # Load with custom .env file
    settings = get_settings(".env.production")
    
    # Check environment
    if settings.is_production():
        print("Running in production mode")
    
    # Get request configuration
    request_config = settings.get_request_config()
    
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

### Environment Variables

Create a `.env` file in your project root:

```bash
# Required
OPENWEATHER_API_KEY=your_api_key_here

# Optional with defaults
WEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
API_TIMEOUT=30
MAX_RETRIES=3
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Configuration Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `api_key` | `str` | Required | OpenWeather API key |
| `base_url` | `str` | `https://api.openweathermap.org/data/2.5` | Base URL for API |
| `timeout` | `int` | `30` | Request timeout in seconds |
| `max_retries` | `int` | `3` | Maximum retry attempts |
| `environment` | `Environment` | `development` | Current environment |
| `log_level` | `str` | `INFO` | Logging level |

## Validation Rules

- **API Key**: Must be non-empty and at least 10 characters
- **Timeout**: Must be between 1 and 300 seconds
- **Max Retries**: Must be between 0 and 10
- **Log Level**: Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Base URL**: Must start with http:// or https://

## Testing the Configuration

Run the configuration module directly to test:

```bash
python -m src.weather_tool.settings
```

This will attempt to load the configuration and print the current settings.

## Migration from Old System

The old `load_api_key()` function is still available for backward compatibility but is deprecated:

```python
# Old way (deprecated)
api_key = load_api_key(".env")

# New way (recommended)
settings = get_settings(".env")
api_key = settings.api_key
```

## Best Practices Demonstrated

1. **Type Safety**: Full type hints throughout the codebase
2. **Documentation**: Comprehensive docstrings for all classes and methods
3. **Error Handling**: Proper exception handling with meaningful messages
4. **Logging**: Professional logging for debugging and monitoring
5. **Validation**: Data validation at the configuration level
6. **Flexibility**: Support for multiple configuration sources
7. **Testing**: Easy to test with different configurations
8. **Maintainability**: Clean, well-structured code that's easy to extend

## Next Steps

This configuration system provides a solid foundation for:
- Adding new configuration fields
- Implementing different configuration sources (database, remote APIs)
- Adding more sophisticated validation rules
- Implementing configuration caching and hot-reloading
- Adding configuration encryption for sensitive data

The patterns demonstrated here are commonly used in enterprise Python applications and will help you transition to senior-level development practices.
