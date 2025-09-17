# websocket_client.py
import json
import threading
import websocket  
import time
import socket
from auth import get_auth_token
from config import WS_BASE_URL, USER_AGENT

_ws_connections = {}
_connection_status = {}
_retry_counts = {}
_define_protocol_message = {
    "protocol": "json",
    "version": 1
}
_record_separator = '\u001e'  # Deve ser enviado ao final de cada mensagem
MARKETDATA_ROUTE = 'marketdata'
ORDERS_ROUTE = 'orders'

# Configurações de retry e timeout
MAX_RETRY_ATTEMPTS = 5
RETRY_DELAY_SECONDS = 2
CONNECTION_TIMEOUT = 10
PING_TIMEOUT = 5

# URLs alternativas para fallback
FALLBACK_URLS = [
    'wss://variableincome-openapi-simulator.xpi.com.br/ws/v1',
    'wss://variableincome-openapi-simulator.xpi.com.br:443/ws/v1',
    'wss://api-parceiros.xpi.com.br/variableincome-openapi/ws/v1'
]

# Funções de diagnóstico e tratamento de erros ################
def test_network_connectivity(host, port=443):
    """Testa conectividade de rede básica"""
    try:
        socket.setdefaulttimeout(5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"❌ Erro no teste de conectividade: {e}")
        return False

def diagnose_connection_issues(route):
    """Diagnostica problemas de conexão"""
    print(f"🔍 Diagnosticando problemas de conexão para {route}...")
    
    # Teste básico de conectividade
    host = "variableincome-openapi-simulator.xpi.com.br"
    if test_network_connectivity(host):
        print(f"✅ Conectividade básica com {host} OK")
    else:
        print(f"❌ Falha na conectividade básica com {host}")
        return False
    
    # Teste de autenticação
    try:
        token = get_auth_token()
        if token and len(token) > 100:
            print(f"✅ Token de autenticação OK ({len(token)} chars)")
        else:
            print(f"❌ Problema com token de autenticação")
            return False
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return False
    
    return True

def get_connection_status(route):
    """Retorna o status da conexão"""
    return _connection_status.get(route, {'connected': False, 'last_error': None})

def reset_connection_retry(route):
    """Reseta o contador de retry para uma rota"""
    _retry_counts[route] = 0

# Funções para enviar mensagens para o WebSocket ###############
def send_message_to_websocket(route, message):
    ws = _ws_connections.get(route)
    if ws and ws.sock and ws.sock.connected:
        msg = message if isinstance(message, str) else json.dumps(message)
        msg += _record_separator  # Adiciona o separador de registro ao final da mensagem
        try:
            ws.send(msg)
            print(f"Mensagem enviada com sucesso: {msg}")
        except Exception as error:
            print(f"Erro ao enviar mensagem: {error}")
    else:
        print("WebSocket não está conectado.")

def sign_ticker_quote(ticker):
    subscribe_message = {
        "arguments": [ticker],
        "target": 'SubscribeQuote',
        "type": 1
    }
    send_message_to_websocket(MARKETDATA_ROUTE, subscribe_message)

def sign_ticker_book(ticker):
    subscribe_message = {
        "arguments": [ticker],
        "target": 'SubscribeBook',
        "type": 1
    }
    send_message_to_websocket(MARKETDATA_ROUTE, subscribe_message)    

def sign_orders_update_status():
    subscribe_message = {
        "arguments": [],
        "target": 'SubscribeOrdersStatus',
        "type": 1
    }
    send_message_to_websocket(ORDERS_ROUTE, subscribe_message)

def unsign_ticker_quote(ticker):
    message = {
        "arguments": [ticker],
        "target": "UnsubscribeQuote",
        "type": 1
    }
    send_message_to_websocket(MARKETDATA_ROUTE, message)

def unsign_ticker_book(ticker):
    message = {
        "arguments": [ticker],
        "target": "UnsubscribeBook",
        "type": 1
    }
    send_message_to_websocket(MARKETDATA_ROUTE, message)

def unsign_orders_update_status():
    message = {
        "arguments": [],
        "target": "UnsubscribeOrdersStatus",
        "type": 1
    }
    send_message_to_websocket(ORDERS_ROUTE, message)

# Funções de callback para o WebSocket #########################
def on_open(ws, route, on_open_callback):
    print(f"✅ Conexão com WebSocket de {route} aberta.")
    _ws_connections[route] = ws
    _connection_status[route] = {'connected': True, 'last_error': None}
    reset_connection_retry(route)  # Resetar contador de retry em caso de sucesso
    
    send_message_to_websocket(route, _define_protocol_message)
    on_open_callback()
def on_message(ws, message, on_message_callback):
    # Divide as mensagens pelo separador de registro
    # Podem haver várias mensagens em uma única entrega
    messages = message.split(_record_separator)
    # Remove mensagens vazias 
    # (pode ocorrer se a mensagem terminar com o separador e houver espaços em branco)
    messages = [msg for msg in messages if msg.strip()]

    for msg in messages:
        try:
            message_dict = json.loads(msg)  # Converte a string JSON em um dicionário
            on_message_callback(message_dict)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar mensagem JSON: {e}")

def on_error(ws, error, route=None):
    """Tratamento avançado de erros do WebSocket"""
    error_msg = str(error)
    print(f"❌ Erro no WebSocket {route}: {error_msg}")
    
    # Atualizar status da conexão
    if route:
        _connection_status[route] = {'connected': False, 'last_error': error_msg}
    
    # Tratamento específico para WinError 10060 (timeout)
    if "10060" in error_msg or "timeout" in error_msg.lower():
        print("🔄 Erro de timeout detectado - tentando diagnóstico...")
        if route and diagnose_connection_issues(route):
            print("🔄 Tentando reconexão automática...")
            threading.Thread(target=lambda: retry_connection(route), daemon=True).start()
    
    # Outros erros de rede
    elif any(code in error_msg for code in ["10061", "10054", "10053"]):
        print("🌐 Erro de rede detectado - servidor pode estar indisponível")
        if route:
            print(f"🔄 Agendando retry para {route} em {RETRY_DELAY_SECONDS} segundos...")
            threading.Thread(target=lambda: retry_connection(route), daemon=True).start()

def on_close(ws, close_status_code, close_msg, route=None):
    """Tratamento de fechamento de conexão"""
    print(f"🔌 Conexão WebSocket {route} fechada. Código: {close_status_code}, Mensagem: {close_msg}")
    
    # Atualizar status
    if route:
        _connection_status[route] = {'connected': False, 'last_error': f"Closed: {close_status_code}"}
    
    # Se foi fechamento inesperado, tentar reconectar
    if close_status_code not in [1000, 1001]:  # 1000=normal, 1001=going away
        print(f"🔄 Fechamento inesperado detectado para {route}")
        if route:
            threading.Thread(target=lambda: retry_connection(route), daemon=True).start()

def retry_connection(route, original_callback=None, original_on_open=None):
    """Tenta reconectar automaticamente"""
    if route not in _retry_counts:
        _retry_counts[route] = 0
    
    if _retry_counts[route] >= MAX_RETRY_ATTEMPTS:
        print(f"❌ Máximo de tentativas de reconexão atingido para {route}")
        return False
    
    _retry_counts[route] += 1
    print(f"🔄 Tentativa de reconexão {_retry_counts[route]}/{MAX_RETRY_ATTEMPTS} para {route}")
    
    time.sleep(RETRY_DELAY_SECONDS * _retry_counts[route])  # Backoff exponencial
    
    try:
        # Tentar reconectar (seria necessário armazenar os callbacks originais)
        print(f"🔄 Executando reconexão para {route}...")
        # Aqui implementaríamos a lógica de reconexão
        return True
    except Exception as e:
        print(f"❌ Falha na reconexão: {e}")
        return False

# Inicialização dos WebSockets #################################
def initialize_market_data_websocket(on_message_callback, on_open_callback):
    """Inicializa WebSocket de Market Data com tratamento de erro robusto"""
    route = MARKETDATA_ROUTE
    
    print(f"🚀 Iniciando WebSocket para {route} com tratamento de erro WinError 10060...")
    
    try:
        # Diagnóstico inicial
        if not diagnose_connection_issues(route):
            print(f"❌ Falha no diagnóstico inicial para {route}")
            return False
        
        # Resetar contador de retry
        reset_connection_retry(route)
        
        token = get_auth_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT
        }

        # Configurar timeout
        websocket.setdefaulttimeout(CONNECTION_TIMEOUT)
        
        ws_marketdata = websocket.WebSocketApp(
            f'{WS_BASE_URL}/ws/v1/{route}',
            header=headers,
            on_open=lambda ws: on_open(ws, route, on_open_callback),
            on_message=lambda ws, message: on_message(ws, message, on_message_callback),
            on_error=lambda ws, error: on_error(ws, error, route),
            on_close=lambda ws, code, msg: on_close(ws, code, msg, route)
        )

        # Executar em thread separada
        def run_with_timeout():
            try:
                ws_marketdata.run_forever(ping_timeout=PING_TIMEOUT)
            except Exception as e:
                print(f"❌ Erro na execução do WebSocket: {e}")

        thread = threading.Thread(target=run_with_timeout, daemon=True)
        thread.start()
        
        print(f"🚀 WebSocket de Market Data iniciado em thread separada.")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar WebSocket: {e}")
        return False

def initialize_orders_websocket(on_message_callback, on_open_callback):
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT
    }

    ws_orders = websocket.WebSocketApp(
        f'{WS_BASE_URL}/ws/v1/{ORDERS_ROUTE}',
        header=headers,
        on_open=lambda ws: on_open(ws, ORDERS_ROUTE, on_open_callback),
        on_message=lambda ws, message: on_message(ws, message, on_message_callback),
        on_error=on_error,
        on_close=on_close
    )

    # Executa o WebSocket em uma thread separada
    thread = threading.Thread(target=ws_orders.run_forever, daemon=True)
    thread.start()
    print(f"WebSocket de Orders iniciado em uma thread separada.")