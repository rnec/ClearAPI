#!/usr/bin/env python3
"""
Teste de conectividade básica para verificar se conseguimos acessar os servidores
"""

import requests
import socket
from urllib.parse import urlparse

def test_http_connectivity():
    """Testar conectividade HTTP"""
    urls = [
        "https://api-parceiros.xpi.com.br/variableincome-openapi-auth/v1/auth",
        "https://variableincome-openapi-simulator.xpi.com.br/api",
        "https://variableincome-openapi-simulator.xpi.com.br"
    ]
    
    for url in urls:
        try:
            print(f"🌐 Testando HTTP: {url}")
            response = requests.get(url, timeout=10)
            print(f"   ✅ Status: {response.status_code}")
        except requests.exceptions.ConnectTimeout:
            print(f"   ❌ Timeout de conexão")
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Erro de conexão: {e}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        print()

def test_websocket_port():
    """Testar se a porta WebSocket está aberta"""
    hosts = [
        ("variableincome-openapi-simulator.xpi.com.br", 443),
        ("variableincome-openapi-simulator.xpi.com.br", 80)
    ]
    
    for host, port in hosts:
        try:
            print(f"🔌 Testando porta {port} em {host}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ Porta {port} está aberta")
            else:
                print(f"   ❌ Porta {port} está fechada ou inacessível")
        except Exception as e:
            print(f"   ❌ Erro ao testar porta: {e}")
        print()

def test_dns_resolution():
    """Testar resolução DNS"""
    hosts = [
        "api-parceiros.xpi.com.br",
        "variableincome-openapi-simulator.xpi.com.br"
    ]
    
    for host in hosts:
        try:
            print(f"🔍 Resolvendo DNS: {host}")
            ip = socket.gethostbyname(host)
            print(f"   ✅ IP: {ip}")
        except Exception as e:
            print(f"   ❌ Erro DNS: {e}")
        print()

if __name__ == "__main__":
    print("🧪 Teste de Conectividade da API XPI")
    print("=" * 50)
    
    print("\n1. Testando resolução DNS...")
    test_dns_resolution()
    
    print("\n2. Testando conectividade HTTP...")
    test_http_connectivity()
    
    print("\n3. Testando portas WebSocket...")
    test_websocket_port()
    
    print("\n✅ Teste concluído!")

