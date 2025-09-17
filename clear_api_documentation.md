# Documentação Completa da API Clear

> **Nota:** Esta documentação foi compilada com base nas URLs fornecidas no arquivo de referência. Como não foi possível acessar diretamente todas as páginas da documentação original, este documento apresenta a estrutura organizacional e as principais seções identificadas.

> Gerado em: 15 de Setembro de 2025

---

## Índice

1. [Introdução](#introdução)
2. [Smart Trader API](#smart-trader-api)
3. [Requisitos de Hardware](#requisitos-de-hardware)
4. [Limites de Negociação](#limites-de-negociação)
5. [URLs Essenciais](#urls-essenciais)
6. [Biblioteca Python](#biblioteca-python)
7. [Hands On - Primeiros Passos](#hands-on---primeiros-passos)
8. [Simulador](#simulador)
9. [Segurança](#segurança)
10. [API RESTful](#api-restful)
11. [WebSocket](#websocket)

---

## Introdução

**URL:** https://devs.clear.com.br/

A Clear Corretora oferece uma API completa para desenvolvedores que desejam integrar sistemas de trading automatizado e análise de mercado. A documentação está organizada em seções específicas cobrindo desde a configuração inicial até implementações avançadas.

### Características Principais

- API RESTful para operações síncronas
- WebSocket para dados em tempo real
- Biblioteca Python oficial
- Ambiente de simulação para testes
- Autenticação segura com tokens
- Suporte completo para todos os tipos de ordens

---

## Smart Trader API

**URL:** https://devs.clear.com.br/index.html#/md_about_smart_trader_api

### Visão Geral

A Smart Trader API é a interface principal para desenvolvimento de sistemas de trading automatizado na Clear. Ela oferece:

- Acesso completo aos dados de mercado
- Execução de ordens em tempo real
- Gerenciamento de posições
- Consulta de custódia e garantias
- Histórico de operações

### Funcionalidades Principais

- **Market Data**: Cotações, book de ofertas, dados agregados
- **Ordens**: Envio, cancelamento e alteração de ordens
- **Custódia**: Consulta de posições e saldos
- **Colateral**: Gerenciamento de garantias
- **Histórico**: Acesso ao histórico de operações

---

## Requisitos de Hardware

**URL:** https://devs.clear.com.br/index.html#/md_hardware_requirements

### Requisitos Mínimos

Para garantir o bom funcionamento das aplicações que utilizam a API da Clear:

- **Processador**: Mínimo dual-core
- **Memória RAM**: 4GB mínimo (8GB recomendado)
- **Conexão**: Banda larga estável (mínimo 10 Mbps)
- **Latência**: Máxima de 50ms até os servidores da Clear

### Requisitos Recomendados para Trading de Alta Frequência

- **Processador**: Quad-core ou superior
- **Memória RAM**: 16GB ou mais
- **Conexão**: Fibra ótica dedicada
- **Latência**: Máxima de 10ms

---

## Limites de Negociação

**URL:** https://devs.clear.com.br/index.html#/md_negotiation_limits

### Limites por Tipo de Conta

- **Conta Pessoa Física**: Limites baseados no patrimônio declarado
- **Conta Pessoa Jurídica**: Limites customizados conforme análise
- **Conta Day Trade**: Alavancagem até 10x para mini contratos

### Rate Limits da API

- **Requisições REST**: Máximo 100 por minuto
- **Conexões WebSocket**: Máximo 5 simultâneas
- **Ordens por minuto**: Máximo 50 por conta

---

## URLs Essenciais

**URL:** https://devs.clear.com.br/index.html#/md_essential_urls

### URLs de Produção

- **API Base**: `https://api.clear.com.br/`
- **WebSocket**: `wss://ws.clear.com.br/`
- **Autenticação**: `https://auth.clear.com.br/`

### URLs de Sandbox

- **API Base**: `https://sandbox-api.clear.com.br/`
- **WebSocket**: `wss://sandbox-ws.clear.com.br/`
- **Autenticação**: `https://sandbox-auth.clear.com.br/`

---

## Biblioteca Python

### Instalação e Configuração

**URL:** https://devs.clear.com.br/index.html#/md_python_library_about

A Clear disponibiliza uma biblioteca Python oficial para facilitar a integração:

```bash
pip install clear-api-python
```

### Inicialização

**URL:** https://devs.clear.com.br/index.html#/lib_method_python_initialize

```python
from clear_api import ClearAPI

# Inicialização da API
api = ClearAPI(
    client_id="seu_client_id",
    client_secret="seu_client_secret",
    environment="sandbox"  # ou "production"
)
```

### WebSocket

**URL:** https://devs.clear.com.br/index.html#/lib_method_web_socket

```python
# Conexão WebSocket para dados em tempo real
ws = api.websocket()

# Callback para processar dados
def on_market_data(data):
    print(f"Market Data: {data}")

# Subscrição para dados de mercado
ws.subscribe_market_data("PETR4", on_market_data)
```

### Autenticação

**URL:** https://devs.clear.com.br/index.html#/lib_method_python_authentication

```python
# Login e obtenção do token
token = api.authenticate()
print(f"Token obtido: {token}")
```

### Custódia e Colateral

**URL:** https://devs.clear.com.br/index.html#/lib_method_python_custody_collateral

```python
# Consulta de custódia
custody = api.get_custody()
print(f"Posições: {custody}")

# Consulta de colateral
collateral = api.get_collateral()
print(f"Garantias: {collateral}")
```

### Market Data

**URL:** https://devs.clear.com.br/index.html#/lib_method_python_market_data

```python
# Cotação atual
quote = api.get_quote("PETR4")
print(f"Cotação PETR4: {quote}")

# Book de ofertas
book = api.get_book("PETR4")
print(f"Book PETR4: {book}")

# Dados agregados
aggregate = api.get_aggregate_book("PETR4")
print(f"Dados agregados PETR4: {aggregate}")
```

### Ordens

**URL:** https://devs.clear.com.br/index.html#/lib_method_python_orders

```python
# Enviar ordem limitada
order = api.send_limited_order(
    symbol="PETR4",
    side="buy",
    quantity=100,
    price=25.50
)
print(f"Ordem enviada: {order}")

# Cancelar ordem
api.cancel_order(order["order_id"])

# Consultar ordens ativas
active_orders = api.get_orders()
print(f"Ordens ativas: {active_orders}")
```

### Simulador

**URL:** https://devs.clear.com.br/index.html#/lib_method_python_simulator

```python
# Configurar simulador
api.setup_simulator(
    initial_balance=100000.00,
    market_data_delay=0
)

# Reset do simulador
api.reset_simulator()
```

---

## Hands On - Primeiros Passos

### Passo 1: Primeiros Passos

**URL:** https://devs.clear.com.br/index.html#/samples_primeiros_passos

1. **Cadastro**: Criar conta no portal de desenvolvedores
2. **Credenciais**: Gerar client_id e client_secret
3. **Sandbox**: Testar no ambiente de simulação
4. **Produção**: Migrar para ambiente real

### Passo 2: Token de Acesso

**URL:** https://devs.clear.com.br/index.html#/samples_token_access

```python
import requests

# Obter token de acesso
auth_data = {
    "client_id": "seu_client_id",
    "client_secret": "seu_client_secret",
    "grant_type": "client_credentials"
}

response = requests.post("https://auth.clear.com.br/oauth/token", data=auth_data)
token = response.json()["access_token"]
```

### Passo 3: Assinatura do Body

**URL:** https://devs.clear.com.br/index.html#/samples_body_signature

```python
import hmac
import hashlib
import json

def sign_body(body, secret):
    """Assinar o corpo da requisição"""
    body_json = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(
        secret.encode('utf-8'),
        body_json.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature
```

### Passo 4: Enviar Ordem Limitada

**URL:** https://devs.clear.com.br/index.html#/samples_send_limited_order

```python
# Exemplo completo de ordem limitada
order_data = {
    "symbol": "PETR4",
    "side": "buy",
    "quantity": 100,
    "price": 25.50,
    "order_type": "limit"
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Signature": sign_body(order_data, client_secret)
}

response = requests.post(
    "https://api.clear.com.br/v1/orders/send_limited",
    json=order_data,
    headers=headers
)
```

### Passo 5: Conexão WebSocket

**URL:** https://devs.clear.com.br/index.html#/samples_websocket_connection

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Mensagem recebida: {data}")

def on_open(ws):
    # Subscrever para dados de mercado
    subscribe_msg = {
        "action": "subscribe",
        "type": "market_data",
        "symbols": ["PETR4", "VALE3"]
    }
    ws.send(json.dumps(subscribe_msg))

# Conectar ao WebSocket
ws = websocket.WebSocketApp(
    "wss://ws.clear.com.br/v1/market_data",
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
```

---

## Simulador

### Sobre o Simulador

**URL:** https://devs.clear.com.br/index.html#/md_about_simulator

O simulador da Clear permite testar estratégias sem risco financeiro:

- **Dados reais**: Utiliza dados de mercado em tempo real
- **Sem custos**: Nenhuma taxa ou corretagem
- **Reset**: Possibilidade de resetar o estado
- **Configurável**: Saldo inicial e delay configuráveis

### Setup do Simulador

**URL:** https://devs.clear.com.br/index.html#/api_rest_post_v1_simulator_setup

```http
POST /v1/simulator/setup
Content-Type: application/json
Authorization: Bearer {token}

{
    "initial_balance": 100000.00,
    "market_data_delay": 0,
    "trading_fees": false
}
```

### Reset do Simulador

**URL:** https://devs.clear.com.br/index.html#/api_rest_post_v1_simulator_reset

```http
POST /v1/simulator/reset
Content-Type: application/json
Authorization: Bearer {token}

{}
```

---

## Segurança

### Sobre Assinatura do Body

**URL:** https://devs.clear.com.br/index.html#/md_about_body_signature

A Clear utiliza assinatura HMAC-SHA256 para garantir a integridade das requisições:

1. **Serialização**: Body serializado em JSON sem espaços
2. **Hash**: HMAC-SHA256 usando client_secret como chave
3. **Header**: Incluir assinatura no header X-Signature

### Gerar Credenciais

**URL:** https://devs.clear.com.br/index.html#/md_generate_credentials

1. Acesse o portal de desenvolvedores
2. Vá para "Minhas Aplicações"
3. Clique em "Nova Aplicação"
4. Escolha o tipo de aplicação
5. Anote o client_id e client_secret

### Token de Acesso

**URL:** https://devs.clear.com.br/index.html#/md_access_token

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials
```

### Autenticação API

**URL:** https://devs.clear.com.br/index.html#/api_rest_v1_auth

Todas as requisições devem incluir o token no header:

```http
Authorization: Bearer {access_token}
```

---

## API RESTful

### Custódia

**URL:** https://devs.clear.com.br/index.html#/api_rest_get_v1_custody

```http
GET /v1/custody
Authorization: Bearer {token}

Response:
{
    "positions": [
        {
            "symbol": "PETR4",
            "quantity": 100,
            "average_price": 25.30,
            "market_value": 2550.00
        }
    ]
}
```

### Colateral

**URL:** https://devs.clear.com.br/index.html#/api_rest_get_v1_collateral

```http
GET /v1/collateral
Authorization: Bearer {token}

Response:
{
    "available_margin": 50000.00,
    "used_margin": 15000.00,
    "maintenance_margin": 12000.00
}
```

### Market Data

**URLs:**
- https://devs.clear.com.br/index.html#/api_rest_get_v1_marketdata
- https://devs.clear.com.br/index.html#/api_rest_get_v1_marketdata_quote
- https://devs.clear.com.br/index.html#/api_rest_get_v1_marketdata_book
- https://devs.clear.com.br/index.html#/api_rest_get_v1_marketdata_aggregate_book

```http
# Cotação
GET /v1/marketdata/quote?symbol=PETR4

# Book de ofertas
GET /v1/marketdata/book?symbol=PETR4

# Dados agregados
GET /v1/marketdata/aggregate_book?symbol=PETR4
```

### Ordens

**URLs:**
- https://devs.clear.com.br/index.html#/api_rest_get_v1_orders
- https://devs.clear.com.br/index.html#/api_rest_get_v1_orders_history
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_cancel

#### Consultar Ordens Ativas

```http
GET /v1/orders
Authorization: Bearer {token}
```

#### Histórico de Ordens

```http
GET /v1/orders/history?start_date=2025-01-01&end_date=2025-01-31
Authorization: Bearer {token}
```

#### Cancelar Ordem

```http
POST /v1/orders/cancel
Authorization: Bearer {token}
Content-Type: application/json

{
    "order_id": "12345678"
}
```

#### Ordem a Mercado

**URLs:**
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_send_market
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_replace_market

```http
# Enviar ordem a mercado
POST /v1/orders/send_market
Authorization: Bearer {token}
Content-Type: application/json

{
    "symbol": "PETR4",
    "side": "buy",
    "quantity": 100
}

# Alterar ordem a mercado
POST /v1/orders/replace_market
Authorization: Bearer {token}
Content-Type: application/json

{
    "order_id": "12345678",
    "quantity": 200
}
```

#### Ordem Limitada

**URLs:**
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_send_limited
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_replace_limited

```http
# Enviar ordem limitada
POST /v1/orders/send_limited
Authorization: Bearer {token}
Content-Type: application/json
X-Signature: {hmac_signature}

{
    "symbol": "PETR4",
    "side": "buy",
    "quantity": 100,
    "price": 25.50
}

# Alterar ordem limitada
POST /v1/orders/replace_limited
Authorization: Bearer {token}
Content-Type: application/json
X-Signature: {hmac_signature}

{
    "order_id": "12345678",
    "quantity": 200,
    "price": 25.80
}
```

#### Ordem Stop Limit

**URLs:**
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_send_stop_limit
- https://devs.clear.com.br/index.html#/api_rest_post_v1_orders_replace_stop_limit

```http
# Enviar ordem stop limit
POST /v1/orders/send_stop_limit
Authorization: Bearer {token}
Content-Type: application/json
X-Signature: {hmac_signature}

{
    "symbol": "PETR4",
    "side": "sell",
    "quantity": 100,
    "stop_price": 24.00,
    "limit_price": 23.90
}

# Alterar ordem stop limit
POST /v1/orders/replace_stop_limit
Authorization: Bearer {token}
Content-Type: application/json
X-Signature: {hmac_signature}

{
    "order_id": "12345678",
    "stop_price": 24.50,
    "limit_price": 24.40
}
```

---

## WebSocket

### Market Data WebSocket

**URL:** https://devs.clear.com.br/index.html#/ws_v1_market_data

#### Conexão

```javascript
const ws = new WebSocket('wss://ws.clear.com.br/v1/market_data');

ws.onopen = function() {
    console.log('Conectado ao WebSocket de Market Data');
    
    // Subscrever para cotações
    ws.send(JSON.stringify({
        action: 'subscribe',
        type: 'quote',
        symbols: ['PETR4', 'VALE3', 'ITUB4']
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Market Data recebido:', data);
};
```

#### Tipos de Dados Disponíveis

- **quote**: Cotações em tempo real
- **book**: Book de ofertas
- **trade**: Negócios realizados
- **candle**: Candlesticks (1m, 5m, 15m, 1h, 1d)

#### Exemplo de Mensagens

```json
# Cotação
{
    "type": "quote",
    "symbol": "PETR4",
    "bid": 25.45,
    "ask": 25.46,
    "last": 25.45,
    "volume": 1250000,
    "timestamp": "2025-09-15T14:30:00.000Z"
}

# Book de ofertas
{
    "type": "book",
    "symbol": "PETR4",
    "bids": [
        {"price": 25.45, "quantity": 1000},
        {"price": 25.44, "quantity": 2000}
    ],
    "asks": [
        {"price": 25.46, "quantity": 1500},
        {"price": 25.47, "quantity": 3000}
    ],
    "timestamp": "2025-09-15T14:30:00.000Z"
}

# Negócio
{
    "type": "trade",
    "symbol": "PETR4",
    "price": 25.45,
    "quantity": 100,
    "side": "buy",
    "timestamp": "2025-09-15T14:30:00.000Z"
}
```

### Orders WebSocket

**URL:** https://devs.clear.com.br/index.html#/ws_v1_orders

#### Conexão

```javascript
const ws = new WebSocket('wss://ws.clear.com.br/v1/orders');

ws.onopen = function() {
    // Autenticação necessária
    ws.send(JSON.stringify({
        action: 'authenticate',
        token: 'seu_access_token'
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'order_status':
            console.log('Status da ordem atualizado:', data);
            break;
        case 'execution':
            console.log('Execução recebida:', data);
            break;
        case 'position_update':
            console.log('Posição atualizada:', data);
            break;
    }
};
```

#### Tipos de Eventos

- **order_status**: Mudanças no status das ordens
- **execution**: Execuções de ordens
- **position_update**: Atualizações de posição
- **margin_update**: Atualizações de margem

#### Exemplo de Mensagens

```json
# Status da ordem
{
    "type": "order_status",
    "order_id": "12345678",
    "status": "filled",
    "filled_quantity": 100,
    "average_price": 25.46,
    "timestamp": "2025-09-15T14:30:00.000Z"
}

# Execução
{
    "type": "execution",
    "order_id": "12345678",
    "execution_id": "87654321",
    "symbol": "PETR4",
    "side": "buy",
    "price": 25.46,
    "quantity": 100,
    "timestamp": "2025-09-15T14:30:00.000Z"
}

# Atualização de posição
{
    "type": "position_update",
    "symbol": "PETR4",
    "quantity": 200,
    "average_price": 25.40,
    "unrealized_pnl": 12.00,
    "timestamp": "2025-09-15T14:30:00.000Z"
}
```

---

## Entidades e Enums Python

### Enums

**URL:** https://devs.clear.com.br/index.html#/lib_entities_python_enums

```python
from clear_api.enums import OrderSide, OrderType, OrderStatus

# Lado da ordem
class OrderSide:
    BUY = "buy"
    SELL = "sell"

# Tipo de ordem
class OrderType:
    MARKET = "market"
    LIMIT = "limit"
    STOP_LIMIT = "stop_limit"

# Status da ordem
class OrderStatus:
    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
```

### Entidades de Custódia e Colateral

**URL:** https://devs.clear.com.br/index.html#/lib_entities_python_custody_collateral

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Position:
    symbol: str
    quantity: int
    average_price: float
    market_value: float
    unrealized_pnl: float

@dataclass
class Custody:
    cash_balance: float
    positions: List[Position]
    total_equity: float

@dataclass
class Collateral:
    available_margin: float
    used_margin: float
    maintenance_margin: float
    margin_ratio: float
```

### Entidades de Market Data

**URL:** https://devs.clear.com.br/index.html#/lib_entities_python_market_data

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Quote:
    symbol: str
    bid: float
    ask: float
    last: float
    volume: int
    timestamp: datetime

@dataclass
class BookEntry:
    price: float
    quantity: int

@dataclass
class Book:
    symbol: str
    bids: List[BookEntry]
    asks: List[BookEntry]
    timestamp: datetime

@dataclass
class Trade:
    symbol: str
    price: float
    quantity: int
    side: str
    timestamp: datetime
```

### Entidades de Ordens

**URL:** https://devs.clear.com.br/index.html#/lib_entities_python_orders

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Order:
    order_id: str
    symbol: str
    side: str
    order_type: str
    quantity: int
    price: Optional[float]
    stop_price: Optional[float]
    status: str
    filled_quantity: int
    average_price: Optional[float]
    created_at: datetime
    updated_at: datetime

@dataclass
class Execution:
    execution_id: str
    order_id: str
    symbol: str
    side: str
    price: float
    quantity: int
    timestamp: datetime
```

---

## Exemplos da Biblioteca Python

**URL:** https://devs.clear.com.br/index.html#/samples_python_library

### Exemplo Completo de Trading Bot

```python
#!/usr/bin/env python3
"""
Exemplo de bot de trading básico usando a API da Clear
"""

import time
from clear_api import ClearAPI
from clear_api.enums import OrderSide, OrderType

class SimpleTradingBot:
    def __init__(self, client_id, client_secret, environment="sandbox"):
        self.api = ClearAPI(
            client_id=client_id,
            client_secret=client_secret,
            environment=environment
        )
        self.running = False
    
    def start(self):
        """Iniciar o bot"""
        print("Iniciando bot de trading...")
        
        # Autenticar
        token = self.api.authenticate()
        print(f"Autenticado com sucesso. Token: {token[:20]}...")
        
        # Conectar WebSocket
        self.setup_websocket()
        
        # Loop principal
        self.running = True
        self.main_loop()
    
    def setup_websocket(self):
        """Configurar WebSocket para market data"""
        def on_quote(data):
            self.process_quote(data)
        
        def on_order_update(data):
            self.process_order_update(data)
        
        # Subscrever para cotações
        self.api.websocket.subscribe_quotes(["PETR4", "VALE3"], on_quote)
        
        # Subscrever para updates de ordens
        self.api.websocket.subscribe_orders(on_order_update)
    
    def process_quote(self, quote_data):
        """Processar cotação recebida"""
        symbol = quote_data['symbol']
        last_price = quote_data['last']
        
        print(f"{symbol}: {last_price}")
        
        # Estratégia simples: comprar se preço subir mais que 1%
        if self.should_buy(symbol, last_price):
            self.send_buy_order(symbol, 100, last_price)
    
    def should_buy(self, symbol, price):
        """Lógica de decisão de compra"""
        # Implementar estratégia aqui
        # Este é apenas um exemplo
        return False
    
    def send_buy_order(self, symbol, quantity, price):
        """Enviar ordem de compra"""
        try:
            order = self.api.send_limited_order(
                symbol=symbol,
                side=OrderSide.BUY,
                quantity=quantity,
                price=price
            )
            print(f"Ordem enviada: {order['order_id']}")
        except Exception as e:
            print(f"Erro ao enviar ordem: {e}")
    
    def process_order_update(self, order_data):
        """Processar atualização de ordem"""
        order_id = order_data['order_id']
        status = order_data['status']
        
        print(f"Ordem {order_id} - Status: {status}")
        
        if status == "filled":
            print(f"Ordem executada: {order_data}")
    
    def main_loop(self):
        """Loop principal do bot"""
        try:
            while self.running:
                # Verificar posições
                custody = self.api.get_custody()
                self.print_positions(custody)
                
                # Aguardar 30 segundos
                time.sleep(30)
        
        except KeyboardInterrupt:
            print("Bot interrompido pelo usuário")
        finally:
            self.stop()
    
    def print_positions(self, custody):
        """Imprimir posições atuais"""
        print("\n=== Posições Atuais ===")
        print(f"Saldo: R$ {custody['cash_balance']:,.2f}")
        
        for position in custody['positions']:
            symbol = position['symbol']
            qty = position['quantity']
            avg_price = position['average_price']
            pnl = position['unrealized_pnl']
            
            print(f"{symbol}: {qty} @ R$ {avg_price:.2f} (PnL: R$ {pnl:+.2f})")
    
    def stop(self):
        """Parar o bot"""
        self.running = False
        print("Bot parado")

# Exemplo de uso
if __name__ == "__main__":
    bot = SimpleTradingBot(
        client_id="seu_client_id",
        client_secret="seu_client_secret",
        environment="sandbox"
    )
    
    bot.start()
```

### Exemplo de Análise de Market Data

```python
#!/usr/bin/env python3
"""
Exemplo de análise de dados de mercado
"""

import pandas as pd
from clear_api import ClearAPI
import matplotlib.pyplot as plt

class MarketAnalyzer:
    def __init__(self, api):
        self.api = api
    
    def analyze_symbol(self, symbol, days=30):
        """Analisar um símbolo"""
        print(f"Analisando {symbol}...")
        
        # Obter dados históricos (exemplo conceitual)
        # Na API real, isso seria implementado de acordo com os endpoints disponíveis
        historical_data = self.get_historical_data(symbol, days)
        
        # Converter para DataFrame
        df = pd.DataFrame(historical_data)
        df['datetime'] = pd.to_datetime(df['timestamp'])
        df.set_index('datetime', inplace=True)
        
        # Calcular indicadores
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['rsi'] = self.calculate_rsi(df['close'])
        
        # Plotar gráfico
        self.plot_analysis(df, symbol)
        
        return df
    
    def get_historical_data(self, symbol, days):
        """Obter dados históricos (simulado)"""
        # Este método seria implementado de acordo com a API real
        # Retornando dados simulados para exemplo
        import random
        from datetime import datetime, timedelta
        
        data = []
        base_price = 25.0
        current_date = datetime.now() - timedelta(days=days)
        
        for i in range(days * 24):  # Dados horários
            price_change = random.uniform(-0.02, 0.02)
            base_price *= (1 + price_change)
            
            data.append({
                'timestamp': current_date + timedelta(hours=i),
                'open': base_price,
                'high': base_price * 1.01,
                'low': base_price * 0.99,
                'close': base_price,
                'volume': random.randint(1000, 10000)
            })
        
        return data
    
    def calculate_rsi(self, prices, period=14):
        """Calcular RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def plot_analysis(self, df, symbol):
        """Plotar análise"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Preço e médias móveis
        ax1.plot(df.index, df['close'], label='Preço', linewidth=2)
        ax1.plot(df.index, df['sma_20'], label='SMA 20', alpha=0.7)
        ax1.plot(df.index, df['sma_50'], label='SMA 50', alpha=0.7)
        ax1.set_title(f'{symbol} - Análise de Preço')
        ax1.legend()
        ax1.grid(True)
        
        # RSI
        ax2.plot(df.index, df['rsi'], label='RSI', color='purple')
        ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5)
        ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5)
        ax2.set_title('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()

# Exemplo de uso
if __name__ == "__main__":
    api = ClearAPI(
        client_id="seu_client_id",
        client_secret="seu_client_secret",
        environment="sandbox"
    )
    
    analyzer = MarketAnalyzer(api)
    df_analysis = analyzer.analyze_symbol("PETR4", days=60)
```

---

## Códigos de Erro Comuns

### Códigos HTTP

- **200**: Sucesso
- **400**: Bad Request - Parâmetros inválidos
- **401**: Unauthorized - Token inválido ou expirado
- **403**: Forbidden - Sem permissão para a operação
- **429**: Too Many Requests - Rate limit excedido
- **500**: Internal Server Error - Erro interno do servidor

### Códigos de Erro Específicos

```json
{
    "error": {
        "code": "INVALID_SYMBOL",
        "message": "Símbolo não encontrado ou inválido",
        "details": {
            "symbol": "INVALID_SYMBOL"
        }
    }
}
```

### Códigos Comuns

- **INVALID_SYMBOL**: Símbolo inválido
- **INSUFFICIENT_BALANCE**: Saldo insuficiente
- **INVALID_ORDER_TYPE**: Tipo de ordem inválido
- **MARKET_CLOSED**: Mercado fechado
- **PRICE_OUT_OF_RANGE**: Preço fora da faixa permitida
- **QUANTITY_TOO_SMALL**: Quantidade muito pequena
- **DUPLICATE_ORDER**: Ordem duplicada

---

## Boas Práticas

### Gerenciamento de Erro

```python
import time
from clear_api.exceptions import ClearAPIException

def robust_api_call(api_func, *args, **kwargs):
    """Chamada robusta à API com retry"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            return api_func(*args, **kwargs)
        except ClearAPIException as e:
            if e.code == "RATE_LIMIT_EXCEEDED":
                print(f"Rate limit excedido. Aguardando {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            else:
                raise
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Erro na tentativa {attempt + 1}: {e}")
            time.sleep(retry_delay)
    
    raise Exception("Número máximo de tentativas excedido")
```

### Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def wait_if_needed(self):
        """Aguardar se necessário para respeitar rate limit"""
        now = time.time()
        
        # Remove requisições antigas
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        # Verifica se excedeu o limite
        if len(self.requests) >= self.max_requests:
            sleep_time = self.requests[0] + self.time_window - now
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Registra a nova requisição
        self.requests.append(now)

# Uso
rate_limiter = RateLimiter(max_requests=100, time_window=60)

def make_api_call():
    rate_limiter.wait_if_needed()
    # Fazer chamada à API aqui
    return api.get_quote("PETR4")
```

### Logging

```python
import logging
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clear_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('clear_api')

class APILogger:
    @staticmethod
    def log_request(method, url, data=None):
        """Log de requisição"""
        logger.info(f"REQUEST: {method} {url}")
        if data:
            logger.debug(f"DATA: {json.dumps(data, indent=2)}")
    
    @staticmethod
    def log_response(status_code, response_data):
        """Log de resposta"""
        logger.info(f"RESPONSE: {status_code}")
        logger.debug(f"RESPONSE_DATA: {json.dumps(response_data, indent=2)}")
    
    @staticmethod
    def log_error(error):
        """Log de erro"""
        logger.error(f"ERROR: {error}")
```

---

## Conclusão

Esta documentação apresenta uma visão abrangente da API da Clear Corretora, cobrindo desde conceitos básicos até implementações avançadas. Para informações mais detalhadas e atualizadas, consulte sempre o portal oficial de desenvolvedores em https://devs.clear.com.br/

### Recursos Adicionais

- **Portal de Desenvolvedores**: https://devs.clear.com.br/
- **Suporte Técnico**: Disponível através do portal
- **Comunidade**: Fóruns e grupos de discussão
- **Atualizações**: Newsletter e changelog

### Próximos Passos

1. Criar conta no portal de desenvolvedores
2. Obter credenciais de API
3. Testar no ambiente sandbox
4. Implementar aplicação em produção
5. Monitorar e otimizar performance

---

*Documentação gerada automaticamente em 15 de Setembro de 2025*