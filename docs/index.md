# ClearAPI Documentation

Bem-vindo à documentação oficial do **ClearAPI** - Sistema de integração com Clear Trading.

## 📚 Documentação Disponível

### Guias de Configuração
- [📖 Configuração Inicial](../README_CONFIG.md)
- [🌐 Interface Web](../README_WEB_INTERFACE.md)
- [📋 Documentação da API](../clear_api_documentation.md)

### Referência da API

#### Autenticação
O ClearAPI utiliza autenticação baseada em tokens OAuth2 com assinatura RSA.

```python
from ClearAPI.auth import authenticate
token = authenticate(client_id, client_secret)
```

#### Cotações em Tempo Real
Obtenha cotações atualizadas via WebSocket ou REST API.

```python
from ClearAPI.get_ticker_quote import get_quote
quote = get_quote('PETR4')
```

#### Execução de Ordens
Sistema completo para envio de ordens de compra e venda.

```python
from ClearAPI.send_order import send_order
order = send_order(
    symbol='PETR4',
    side='buy',
    quantity=100,
    price=25.50
)
```

## 🚀 Início Rápido

1. **Instalação**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuração**
   ```bash
   cp clear_api_config.env.example clear_api_config.env
   # Edite com suas credenciais
   ```

3. **Teste de Conectividade**
   ```bash
   python test_connectivity.py
   ```

4. **Iniciar Dashboard**
   ```bash
   python start_web_dashboard.py
   ```

## 📊 Funcionalidades

### Dashboard Web
- Interface moderna e responsiva
- Gráficos em tempo real
- Monitoramento de posições
- Histórico de operações

### API REST
- Endpoints completos para trading
- Documentação OpenAPI/Swagger
- Rate limiting e controle de acesso
- Logs detalhados de operações

### WebSocket
- Cotações em tempo real
- Updates de posições
- Notificações de ordens executadas
- Reconexão automática

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```env
CLIENT_ID=seu_client_id
ACCESS_TOKEN=seu_access_token
REFRESH_TOKEN=seu_refresh_token
BASE_URL=https://api.clear.com.br
DEBUG=false
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 📞 Suporte

- **GitHub Issues**: [Reportar problemas](https://github.com/rnec/ClearAPI/issues)
- **Email**: rnectrade@gmail.com
- **Documentação**: [GitHub Pages](https://rnec.github.io/ClearAPI/)

---

© 2024 ClearAPI - Sistema de Trading Automatizado
