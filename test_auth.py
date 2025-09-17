#!/usr/bin/env python3
"""
Teste de autenticação para verificar se as credenciais funcionam
"""

import sys
import os

# Adiciona o diretório ClearAPI ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ClearAPI'))

from auth import get_auth_token

print("🧪 Testando autenticação...")

try:
    token = get_auth_token()
    if token:
        print("✅ Autenticação funcionou!")
        print(f"Token obtido: {token[:20]}...")
    else:
        print("❌ Token vazio ou inválido!")
except Exception as e:
    print(f"❌ Erro na autenticação: {e}")