# quote_monitor.py
# Monitor simples de cotações em tempo real via WebSocket

import json
import sys
import os
from datetime import datetime
from time import sleep
import signal
import threading

# Adiciona o diretório ClearAPI ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ClearAPI'))

try:
    # pylint: disable=import-error
    # Os módulos estão no diretório ClearAPI/ que é adicionado ao sys.path
    from websocket_client import initialize_market_data_websocket, sign_ticker_quote  # pylint: disable=import-error
    from get_ticker_quote import get_ticker_quote  # pylint: disable=import-error
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("📁 Verifique se os arquivos estão no diretório ClearAPI/")
    print("📋 Arquivos necessários: websocket_client.py, get_ticker_quote.py")
    sys.exit(1)

# Configuração
TICKER = "WINV25"  # Altere aqui para o ativo desejado
IS_RUNNING = True
websocket_connection = None

def format_timestamp():
    """Formata o timestamp atual"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def print_table_header():
    """Imprime o cabeçalho da tabela"""
    print("=" * 70)
    print(f"{'Timestamp':<24} {'Ativo':<10} {'Cotação':<15}")
    print("=" * 70)

def print_quote_row(timestamp, ticker, price):
    """Imprime uma linha com a cotação"""
    print(f"{timestamp:<24} {ticker:<10} {price:<15.4f}")

def on_message(message):
    """Processa mensagens recebidas do WebSocket"""
    try:
        # O websocket_client já converte para dict, então message já é um dicionário
        if not message:
            return
        
        # Verifica se é uma mensagem de cotação
        if message.get('target') == 'Quote' and message.get('arguments'):
            try:
                quote_data = message['arguments'][0]
                ticker = quote_data.get('ticker')
                last_price = quote_data.get('lastPrice')
                
                if ticker and last_price is not None:
                    timestamp = format_timestamp()
                    print_quote_row(timestamp, ticker, last_price)
                else:
                    print(f"⚠️ Dados de cotação incompletos: ticker={ticker}, price={last_price}")
            except (IndexError, KeyError, TypeError) as e:
                print(f"⚠️ Erro ao processar dados de cotação: {e}")
                print(f"📝 Dados recebidos: {message.get('arguments', 'N/A')}")
        else:
            # Debug: mostra outros tipos de mensagem (apenas se não for heartbeat)
            target = message.get('target', 'Unknown')
            if target not in ['', 'ping', 'pong', 'heartbeat']:
                print(f"📨 Mensagem recebida: {target}")
                
    except Exception as e:
        print(f"❌ Erro crítico ao processar mensagem: {e}")
        print(f"📝 Mensagem completa: {message}")
        import traceback
        traceback.print_exc()

def on_open():
    """Executado quando a conexão WebSocket é aberta"""
    print(f"WebSocket conectado! Assinando ticker: {TICKER}")
    try:
        # Usa a função do websocket_client para assinar cotações
        sign_ticker_quote(TICKER)
        print(f"✅ Assinatura do ticker {TICKER} realizada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao assinar ticker {TICKER}: {e}")

def signal_handler(signum, frame):
    """Manipula sinais de interrupção para encerramento gracioso"""
    global IS_RUNNING
    print("\n" + "=" * 70)
    print("🛑 Sinal de interrupção recebido. Encerrando monitor...")
    IS_RUNNING = False
    
def stop_monitor():
    """Para o monitor de forma gracioso"""
    global IS_RUNNING
    IS_RUNNING = False
    print("🛑 Parando monitor de cotações...")

def main():
    """Função principal"""
    global IS_RUNNING, websocket_connection
    
    # Configura manipulador de sinais para encerramento gracioso
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"🚀 Iniciando monitor de cotações para {TICKER}")
    print("💡 Pressione Ctrl+C para encerrar o monitor")
    print_table_header()
    
    try:
        # Conecta ao WebSocket usando a função do websocket_client
        print("🔄 Inicializando conexão WebSocket...")
        websocket_success = initialize_market_data_websocket(on_message, on_open)
        
        if not websocket_success:
            print("❌ Falha ao inicializar WebSocket. Verifique a configuração.")
            return
        
        print("⏳ Aguardando conexão e mensagens...")
        print("💡 Para parar o monitor, pressione Ctrl+C")
        
        # Mantém o script rodando enquanto IS_RUNNING for True
        while IS_RUNNING:
            sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("🛑 Monitor encerrado pelo usuário (Ctrl+C).")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        IS_RUNNING = False
        print("🧹 Limpando recursos...")
        print("✅ Monitor encerrado com sucesso.")

if __name__ == "__main__":
    main()
