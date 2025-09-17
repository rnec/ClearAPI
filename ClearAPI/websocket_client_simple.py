# websocket_client_simple.py
# Implementação simples baseada na documentação original da Clear
import websocket as ws
import json
import threading
import time
from auth import get_auth_token
from config import WS_BASE_URL

# Variável global para armazenar a conexão
ws_connection = None

def create_websocket_connection(on_message_callback, on_open_callback):
    """
    Cria uma conexão WebSocket simples baseada na documentação original
    """
    global ws_connection
    
    try:
        token = get_auth_token()
        # URL baseada na documentação: wss://ws.clear.com.br/v1/market_data
        # Mas usando o servidor de simulação da XPI
        url = f"{WS_BASE_URL}/v1/market_data"
        
        print(f"🔗 Conectando ao WebSocket: {url}")
        
        def on_message(ws, message):
            print(f"📨 Mensagem recebida: {message[:200]}...")
            on_message_callback(message)
        
        def on_open(ws):
            print("✅ WebSocket conectado com sucesso!")
            on_open_callback(ws)
        
        def on_error(ws, error):
            print(f"❌ Erro no WebSocket: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print(f"🔌 WebSocket fechado. Status: {close_status_code}, Msg: {close_msg}")
        
        # Headers de autenticação
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Smart-Trader-API Devs-Clear'
        }
        
        # Criar conexão WebSocket
        ws_connection = ws.WebSocketApp(
            url,
            header=headers,
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
            on_close=on_close
        )
        
        # Executar em thread separada
        def run_websocket():
            ws_connection.run_forever()
        
        thread = threading.Thread(target=run_websocket)
        thread.daemon = True
        thread.start()
        
        # Dar tempo para a conexão ser estabelecida
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Erro ao conectar WebSocket: {e}")
        raise

def send_subscription_message(symbols):
    """
    Envia mensagem de subscrição baseada na documentação original
    """
    global ws_connection
    
    if ws_connection and ws_connection.sock and ws_connection.sock.connected:
        # Formato baseado na documentação
        subscribe_msg = {
            "action": "subscribe",
            "type": "market_data", 
            "symbols": symbols if isinstance(symbols, list) else [symbols]
        }
        
        message = json.dumps(subscribe_msg)
        print(f"📤 Enviando subscrição: {message}")
        
        try:
            ws_connection.send(message)
            print("✅ Mensagem de subscrição enviada")
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
    else:
        print("❌ WebSocket não está conectado")

# Função de compatibilidade para o quote_monitor.py
def connect_websocket(on_message_callback, on_open_callback, route):
    """
    Função de compatibilidade para manter a interface existente
    """
    def simple_on_open(ws):
        on_open_callback()
    
    create_websocket_connection(on_message_callback, simple_on_open)

def send_message_to_websocket(route, message):
    """
    Função de compatibilidade para enviar mensagens
    """
    if hasattr(message, 'arguments') and hasattr(message, 'target'):
        # Se é uma WebSocketRequestMessage, converter para formato simples
        if message.target == 'SubscribeQuote':
            send_subscription_message(message.arguments)
    else:
        print(f"⚠️ Tipo de mensagem não suportado: {message}")

class WebSocketRequestMessage:
    """
    Classe para compatibilidade
    """
    def __init__(self, arguments, target, msg_type):
        self.arguments = arguments
        self.target = target
        self.type = msg_type
