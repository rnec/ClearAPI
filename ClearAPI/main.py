# main.py
# Exemplo de uso da API de Smart Trading com websocket e autenticação

from time import sleep
from colorama import Fore, Style
from auth import get_auth_token
from signature import generate_body_signature
from websocket_client import connect_websocket, send_message_to_websocket, WebSocketRequestMessage
from get_ticker_quote import get_ticker_quote

TICKER = "WDOV25"
IS_RUNNING = True

print(Fore.CYAN + f"Ticker carregado: {TICKER}" + Style.RESET_ALL)

# 1 - Itens de segurança ###############################################
token = get_auth_token()
body_signature = generate_body_signature({ 'teste': 'teste' })

# 2 - Consultar cotação de um ativo
# 
ticker_quote = get_ticker_quote(TICKER)
print(Fore.GREEN + f"Último preço do {TICKER}: R$ {ticker_quote['lastPrice']:.4f}" + Style.RESET_ALL)

# 3 - Conexão com websocket ##########################################
def market_data_callback(message):
    print(Fore.BLUE + f"Mensagem recebida: {message}" + Style.RESET_ALL)  # Debug
    if message.get('target') == 'Quote':
        #print(Fore.CYAN + "Mensagem é do tipo Quote" + Style.RESET_ALL)  # Debug
        last_price = message.get('arguments')[0].get('lastPrice')
        if last_price:
            print(Fore.MAGENTA + f"Nova cotação {TICKER}: {last_price:.4f}" + Style.RESET_ALL)
            simple_trading_strategy(last_price)
    else:
        print(Fore.RED + f"Mensagem não é Quote. Target: {message.get('target')}" + Style.RESET_ALL)  # Debug

def on_market_data_open_callback():
    print(Fore.YELLOW + f"WebSocket conectado! Assinando ticker: {TICKER}" + Style.RESET_ALL)  # Debug
    sign_ticker_quote(TICKER) # Assinando o ticker

initialize_market_data_websocket(market_data_callback, on_market_data_open_callback)

while IS_RUNNING:
    sleep(0.1)  # Manter o script em execução para receber mensagens do WebSocket