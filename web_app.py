"""
FastAPI Web Application para monitoramento de cotações em tempo real
Integra com a ClearAPI para dados de mercado via WebSocket
"""

import asyncio
import json
import sys
import os
from typing import Dict, Set, List
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Adiciona o diretório ClearAPI ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ClearAPI'))
from websocket_client import initialize_market_data_websocket, sign_ticker_quote, send_message_to_websocket, unsign_ticker_quote  # pylint: disable=import-error
from get_ticker_quote import get_ticker_quote  # pylint: disable=import-error
from send_order import SendMarketOrderRequest, send_market_order  # pylint: disable=import-error

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Clear Trading Dashboard",
    description="Dashboard em tempo real para monitoramento de cotações",
    version="1.0.0"
)

# Configuração de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Gerenciamento de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscribed_tickers: Set[str] = set()
        self.clear_ws_connected = False
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    async def broadcast(self, message: str):
        # Cria uma cópia da lista para evitar modificação durante iteração
        connections_copy = self.active_connections.copy()
        dead_connections = []
        
        for connection in connections_copy:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"⚠️ Conexão morta detectada: {e}")
                # Marca para remoção posterior
                dead_connections.append(connection)
        
        # Remove conexões mortas após a iteração
        for dead_conn in dead_connections:
            if dead_conn in self.active_connections:
                self.active_connections.remove(dead_conn)
                
    async def subscribe_ticker(self, ticker: str):
        """Adiciona um ticker à lista de monitoramento"""
        if ticker not in self.subscribed_tickers:
            self.subscribed_tickers.add(ticker)
            if self.clear_ws_connected:
                # Assina o ticker na ClearAPI usando a função do websocket_client
                sign_ticker_quote(ticker)
                
    async def unsubscribe_ticker(self, ticker: str):
        """Remove um ticker da lista de monitoramento"""
        if ticker in self.subscribed_tickers:
            self.subscribed_tickers.discard(ticker)
            if self.clear_ws_connected:
                # Desassina o ticker na ClearAPI usando a função do websocket_client
                unsign_ticker_quote(ticker)

manager = ConnectionManager()

def format_timestamp():
    """Formata o timestamp atual"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def on_clear_message(message):
    """Processa mensagens recebidas do WebSocket da ClearAPI"""
    try:
        # Verifica se message é string ou dict
        if isinstance(message, dict):
            data = message
        elif isinstance(message, str):
            if not message.strip():
                return
            print(f"📨 Mensagem recebida da ClearAPI: {message[:100]}...")  # Debug
            data = json.loads(message)
        else:
            print(f"⚠️ Tipo de mensagem desconhecido: {type(message)}")
            return
        
        # Verifica se é uma mensagem de cotação
        if data.get('target') == 'Quote' and data.get('arguments'):
            try:
                quote_data = data['arguments'][0]
                ticker = quote_data.get('ticker')
                last_price = quote_data.get('lastPrice')
            except (IndexError, KeyError, TypeError) as e:
                print(f"⚠️ Erro ao processar dados de cotação: {e}")
                print(f"📝 Dados recebidos: {data.get('arguments', 'N/A')}")
                return
            
            print(f"💰 Cotação recebida: {ticker} = {last_price}")  # Debug
            
            if ticker and last_price is not None:
                # Sempre processa a cotação, mesmo se não estiver na lista de subscritos
                # Isso permite receber dados mesmo antes da subscrição ser confirmada
                
                # Adiciona à lista de subscritos se não estiver
                if ticker not in manager.subscribed_tickers:
                    manager.subscribed_tickers.add(ticker)
                
                # Prepara dados para enviar ao frontend
                quote_message = {
                    'type': 'quote_update',
                    'data': {
                        'ticker': ticker,
                        'lastPrice': last_price,
                        'timestamp': format_timestamp(),
                        'bid': quote_data.get('bid'),
                        'ask': quote_data.get('ask'),
                        'volume': quote_data.get('volume'),
                        'change': quote_data.get('change', 0),
                        'changePercent': quote_data.get('changePercent', 0)
                    }
                }
                
                print(f"📤 Enviando dados para frontend: {ticker}")  # Debug
                
                # Envia para todos os clientes conectados usando thread-safe approach
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.create_task(manager.broadcast(json.dumps(quote_message)))
                    else:
                        # Se não há loop rodando, agenda para execução
                        asyncio.run_coroutine_threadsafe(
                            manager.broadcast(json.dumps(quote_message)), 
                            loop
                        )
                except RuntimeError:
                    # Se não há event loop, cria um novo
                    import threading
                    def broadcast_in_thread():
                        try:
                            asyncio.run(manager.broadcast(json.dumps(quote_message)))
                        except Exception as e:
                            print(f"❌ Erro ao enviar broadcast: {e}")
                    
                    thread = threading.Thread(target=broadcast_in_thread, daemon=True)
                    thread.start()
        else:
            print(f"📋 Mensagem não é Quote: {data.get('target', 'unknown')}")  # Debug
                
    except json.JSONDecodeError as e:
        print(f"⚠️ Erro JSON: {e}")
        if isinstance(message, str):
            print(f"📝 Mensagem: {message[:100]}...")
        else:
            print(f"📝 Mensagem: {type(message)} - {str(message)[:100]}...")
    except Exception as e:
        print(f"❌ Erro crítico ao processar mensagem da ClearAPI: {e}")
        if isinstance(message, str):
            print(f"📝 Mensagem: {message[:100]}...")
        else:
            print(f"📝 Tipo: {type(message)}, Conteúdo: {str(message)[:100]}...")
        import traceback
        traceback.print_exc()

def on_clear_open():
    """Executado quando a conexão WebSocket da ClearAPI é aberta"""
    manager.clear_ws_connected = True
    print("🎉 Conexão com ClearAPI WebSocket estabelecida com sucesso!")
    
    # Assina todos os tickers já cadastrados
    if manager.subscribed_tickers:
        print(f"📝 Resubscrevendo {len(manager.subscribed_tickers)} tickers...")
        for ticker in manager.subscribed_tickers:
            try:
                sign_ticker_quote(ticker)
                print(f"✅ Subscrito: {ticker}")
            except Exception as e:
                print(f"❌ Erro ao subscrever {ticker}: {e}")
    else:
        print("📋 Nenhum ticker para subscrever no momento")

# Inicializa conexão com ClearAPI ao iniciar a aplicação
@app.on_event("startup")
async def startup_event():
    """Conecta ao WebSocket da ClearAPI quando a aplicação inicia"""
    import asyncio
    import threading
    
    def start_clear_websocket():
        """Inicia a conexão WebSocket da ClearAPI em thread separada"""
        try:
            initialize_market_data_websocket(on_clear_message, on_clear_open)
            print("✅ Conexão com ClearAPI WebSocket iniciada com sucesso")
        except Exception as e:
            print(f"❌ Erro ao conectar com ClearAPI: {e}")
    
    # Executa a conexão em thread separada para não bloquear o startup
    thread = threading.Thread(target=start_clear_websocket, daemon=True)
    thread.start()
    print("🔄 Iniciando conexão com ClearAPI WebSocket...")

# Rotas da aplicação
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """Página principal do dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/quote/{ticker}")
async def get_quote(ticker: str):
    """Endpoint para obter cotação atual de um ticker"""
    try:
        quote = get_ticker_quote(ticker)
        return {
            "success": True,
            "data": quote
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/order/market")
async def send_order_market(request: Request):
    """Endpoint para enviar ordem a mercado"""
    try:
        data = await request.json()
        
        # Valida os dados recebidos
        required_fields = ['ticker', 'side', 'quantity']
        for field in required_fields:
            if field not in data:
                return {
                    "success": False,
                    "error": f"Campo obrigatório ausente: {field}"
                }
        
        # Cria o objeto de requisição
        order_request = SendMarketOrderRequest(
            module='DayTrade',  # Por enquanto apenas DayTrade está disponível
            ticker=data['ticker'].upper(),
            side=data['side'],  # 'Buy' ou 'Sell'
            quantity=int(data['quantity']),
            time_in_force='Day'  # Padrão para ordens a mercado
        )
        
        # Envia a ordem
        response = send_market_order(order_request)
        
        return {
            "success": True,
            "data": {
                "orderId": response.order_id,
                "message": f"Ordem {data['side'].lower()} de {data['quantity']} {data['ticker']} enviada com sucesso"
            }
        }
        
    except ValueError as e:
        return {
            "success": False,
            "error": f"Erro de validação: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erro ao enviar ordem: {str(e)}"
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicação em tempo real com o frontend"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Recebe mensagens do cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message['type'] == 'subscribe':
                # Cliente quer se inscrever em um ticker
                ticker = message['ticker'].upper()
                await manager.subscribe_ticker(ticker)
                
                # Envia confirmação
                await manager.send_personal_message(
                    json.dumps({
                        'type': 'subscription_confirmed',
                        'ticker': ticker
                    }),
                    websocket
                )
                
            elif message['type'] == 'unsubscribe':
                # Cliente quer cancelar inscrição de um ticker
                ticker = message['ticker'].upper()
                await manager.unsubscribe_ticker(ticker)
                
                # Envia confirmação
                await manager.send_personal_message(
                    json.dumps({
                        'type': 'unsubscription_confirmed',
                        'ticker': ticker
                    }),
                    websocket
                )
                
            elif message['type'] == 'get_subscribed':
                # Cliente quer saber quais tickers estão sendo monitorados
                await manager.send_personal_message(
                    json.dumps({
                        'type': 'subscribed_tickers',
                        'tickers': list(manager.subscribed_tickers)
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
