#!/usr/bin/env python3
"""
Teste simples do WebSocket com implementação baseada na documentação original
"""

import sys
import os
import json
from time import sleep

# Adiciona o diretório ClearAPI ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ClearAPI'))

from websocket_client_simple import create_websocket_connection, send_subscription_message

def on_message(message):
    """Processa mensagens recebidas"""
    try:
        if message.strip():
            data = json.loads(message)
            print(f"📊 Dados recebidos: {data}")
    except json.JSONDecodeError as e:
        print(f"⚠️ Erro ao decodificar JSON: {e}")
        print(f"📝 Mensagem bruta: {message}")

def on_open(ws):
    """Executado quando conecta"""
    print("🚀 Conectado! Enviando subscrição...")
    # Aguarda um pouco antes de enviar a subscrição
    sleep(1)
    send_subscription_message(["WINV25", "PETR4"])

def main():
    print("🧪 Testando WebSocket simples...")
    
    try:
        create_websocket_connection(on_message, on_open)
        
        print("⏳ Aguardando mensagens... (Ctrl+C para sair)")
        while True:
            sleep(1)
            
    except KeyboardInterrupt:
        print("\n✅ Teste encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
