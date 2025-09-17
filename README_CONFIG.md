# Configuração da API Clear

Este documento explica como configurar e usar as variáveis de ambiente para a API Clear.

## Arquivos de Configuração

### `clear_api_config.env`
Arquivo que contém todas as variáveis de ambiente necessárias para a API Clear.

### `config.py`
Módulo Python que carrega e gerencia as configurações.

## Configuração Inicial

### 1. Instalar Dependências

```bash
pip install python-dotenv
```

### 2. Configurar Credenciais

1. Acesse o portal de desenvolvedores: https://devs.clear.com.br/
2. Crie uma nova aplicação
3. Anote seu `CLIENT_ID` e `CLIENT_SECRET`
4. Edite o arquivo `clear_api_config.env` e substitua:
   - `seu_client_id_aqui` pelo seu CLIENT_ID
   - `seu_client_secret_aqui` pelo seu CLIENT_SECRET

### 3. Escolher Ambiente

No arquivo `clear_api_config.env`, configure a variável `ENVIRONMENT`:
- `sandbox` - Para testes (padrão)
- `production` - Para ambiente real

## Variáveis de Ambiente Disponíveis

### Credenciais
- `CLIENT_ID`: ID do cliente fornecido pela Clear
- `CLIENT_SECRET`: Chave secreta fornecida pela Clear

### Ambiente
- `ENVIRONMENT`: Ambiente de execução (sandbox/production)

### URLs da API
**Sandbox:**
- `SANDBOX_API_BASE_URL`: URL base da API de sandbox
- `SANDBOX_WEBSOCKET_URL`: URL do WebSocket de sandbox
- `SANDBOX_AUTH_URL`: URL de autenticação de sandbox

**Produção:**
- `PRODUCTION_API_BASE_URL`: URL base da API de produção
- `PRODUCTION_WEBSOCKET_URL`: URL do WebSocket de produção
- `PRODUCTION_AUTH_URL`: URL de autenticação de produção

### Rate Limiting
- `MAX_REQUESTS_PER_MINUTE`: Máximo de requisições por minuto (padrão: 100)
- `MAX_WEBSOCKET_CONNECTIONS`: Máximo de conexões WebSocket (padrão: 5)
- `MAX_ORDERS_PER_MINUTE`: Máximo de ordens por minuto (padrão: 50)

### Simulador
- `SIMULATOR_INITIAL_BALANCE`: Saldo inicial do simulador
- `SIMULATOR_MARKET_DATA_DELAY`: Delay dos dados de mercado
- `SIMULATOR_TRADING_FEES`: Se deve aplicar taxas de negociação

### Configurações de Rede
- `REQUEST_TIMEOUT`: Timeout para requisições HTTP (segundos)
- `WEBSOCKET_TIMEOUT`: Timeout para conexões WebSocket (segundos)

### Configurações de Retry
- `MAX_RETRIES`: Número máximo de tentativas em caso de erro
- `RETRY_DELAY`: Delay entre tentativas (segundos)

### Logging
- `LOG_LEVEL`: Nível de log (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Arquivo de log

### Trading
- `DEFAULT_SYMBOLS`: Símbolos padrão para monitoramento (separados por vírgula)
- `DEFAULT_ORDER_QUANTITY`: Quantidade padrão para ordens
- `MAX_POSITION_SIZE`: Tamanho máximo de posição

## Uso no Código Python

### Importar Configuração

```python
from config import config, get_config

# Usar a instância global
print(f"Ambiente: {config.environment}")
print(f"API URL: {config.api_base_url}")

# Ou obter uma nova instância
my_config = get_config()
```

### Verificar Credenciais

```python
if config.validate_credentials():
    print("Credenciais configuradas corretamente")
else:
    print("ERRO: Credenciais não configuradas")
```

### Obter URLs Baseadas no Ambiente

```python
# As URLs são automaticamente selecionadas baseadas no ambiente
api_url = config.api_base_url
ws_url = config.websocket_url
auth_url = config.auth_url
```

### Obter Dados de Autenticação

```python
auth_data = config.get_auth_data()
# Retorna: {"client_id": "...", "client_secret": "...", "grant_type": "client_credentials"}
```

### Obter Headers para Requisições

```python
headers = config.get_headers()
# Inclui automaticamente o token se disponível
```

### Verificar Ambiente

```python
if config.is_sandbox():
    print("Executando no ambiente de sandbox")
elif config.is_production():
    print("Executando no ambiente de produção")
```

## Exemplo de Uso Completo

```python
from config import config
import requests

# Verificar configuração
if not config.validate_credentials():
    raise ValueError("Credenciais não configuradas")

# Fazer autenticação
auth_data = config.get_auth_data()
response = requests.post(
    f"{config.auth_url}/oauth/token",
    data=auth_data,
    timeout=config.request_timeout
)

if response.status_code == 200:
    token_data = response.json()
    config.access_token = token_data["access_token"]
    print("Autenticado com sucesso!")
else:
    print(f"Erro na autenticação: {response.status_code}")

# Fazer requisição à API
headers = config.get_headers()
response = requests.get(
    f"{config.api_base_url}/v1/custody",
    headers=headers,
    timeout=config.request_timeout
)

print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}")
```

## Segurança

⚠️ **IMPORTANTE**: 
- Nunca commite o arquivo com suas credenciais reais
- Use diferentes credenciais para sandbox e produção
- Mantenha o `CLIENT_SECRET` seguro
- Considere usar um gerenciador de segredos em produção

## Recarregar Configuração

Se você modificar o arquivo `.env` durante a execução:

```python
from config import reload_config

# Recarrega as configurações
new_config = reload_config()
```

## Troubleshooting

### Erro: "Credenciais não configuradas"
- Verifique se o arquivo `clear_api_config.env` existe
- Confirme se `CLIENT_ID` e `CLIENT_SECRET` estão preenchidos
- Certifique-se de que não há espaços extras nas variáveis

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Erro de autenticação
- Verifique se as credenciais estão corretas
- Confirme se está usando o ambiente correto (sandbox/production)
- Verifique se as URLs estão corretas
