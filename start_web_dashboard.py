#!/usr/bin/env python3
"""
Script de inicialização para o Clear Trading Dashboard
Facilita a execução da interface web com verificações de ambiente
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'websockets',
        'jinja2',
        'aiofiles',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - não encontrado")
    
    if missing_packages:
        print(f"\n📦 Instalando dependências faltantes...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar dependências")
            print("   Tente executar manualmente: pip install -r requirements.txt")
            return False
    
    return True

def check_config_file():
    """Verifica se o arquivo de configuração existe"""
    config_file = Path("clear_api_config.env")
    if config_file.exists():
        print("✅ Arquivo de configuração encontrado")
        return True
    else:
        print("⚠️  Arquivo clear_api_config.env não encontrado")
        print("   Certifique-se de configurar suas credenciais da ClearAPI")
        return False

def check_clearapi_modules():
    """Verifica se os módulos da ClearAPI estão disponíveis"""
    clearapi_path = Path("ClearAPI")
    required_files = [
        "auth.py",
        "websocket_client.py", 
        "get_ticker_quote.py",
        "config.py"
    ]
    
    if not clearapi_path.exists():
        print("❌ Pasta ClearAPI não encontrada")
        return False
    
    missing_files = []
    for file in required_files:
        if not (clearapi_path / file).exists():
            missing_files.append(file)
            print(f"❌ ClearAPI/{file} - não encontrado")
        else:
            print(f"✅ ClearAPI/{file}")
    
    if missing_files:
        print(f"\n❌ Arquivos da ClearAPI faltando: {', '.join(missing_files)}")
        return False
    
    return True

def check_frontend_files():
    """Verifica se os arquivos do frontend estão presentes"""
    frontend_files = [
        "frontend/templates/dashboard.html",
        "frontend/static/js/dashboard.js",
        "frontend/static/css/dashboard.css"
    ]
    
    missing_files = []
    for file in frontend_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"❌ {file} - não encontrado")
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"\n❌ Arquivos do frontend faltando: {', '.join(missing_files)}")
        return False
    
    return True

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Inicia o servidor FastAPI"""
    print(f"\n🚀 Iniciando servidor em http://{host}:{port}")
    print("   Pressione Ctrl+C para parar o servidor")
    print("   O dashboard estará disponível no navegador")
    
    try:
        import uvicorn
        uvicorn.run(
            "web_app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("🔍 Clear Trading Dashboard - Verificação de Sistema\n")
    
    # Verificações do sistema
    checks = [
        ("Versão do Python", check_python_version),
        ("Dependências Python", check_dependencies),
        ("Arquivo de configuração", check_config_file),
        ("Módulos ClearAPI", check_clearapi_modules),
        ("Arquivos do frontend", check_frontend_files)
    ]
    
    all_checks_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 Verificando {check_name}:")
        if not check_func():
            all_checks_passed = False
    
    print("\n" + "="*50)
    
    if not all_checks_passed:
        print("❌ Algumas verificações falharam")
        print("   Corrija os problemas acima antes de continuar")
        return False
    
    print("✅ Todas as verificações passaram!")
    
    # Pergunta se quer iniciar o servidor
    try:
        response = input("\n🚀 Deseja iniciar o servidor agora? (s/N): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            # Pequena pausa para melhor UX
            time.sleep(1)
            return start_server()
        else:
            print("\n💡 Para iniciar manualmente:")
            print("   python web_app.py")
            print("   ou")
            print("   uvicorn web_app:app --host 0.0.0.0 --port 8000 --reload")
            return True
    except KeyboardInterrupt:
        print("\n👋 Saindo...")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
