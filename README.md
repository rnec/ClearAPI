# ClearAPI - Trading API Integration

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descrição

**ClearAPI** é um sistema completo de integração com a API da Clear Trading, oferecendo funcionalidades avançadas para monitoramento de mercado, execução de ordens e gerenciamento de portfólio através de uma interface web moderna e intuitiva.

## ✨ Funcionalidades Principais

- 🔐 **Autenticação Segura** - Sistema de autenticação com chaves RSA
- 📊 **Dashboard Web** - Interface moderna para monitoramento em tempo real
- 📈 **Cotações em Tempo Real** - WebSocket para dados de mercado atualizados
- 🛒 **Execução de Ordens** - Sistema completo para envio de ordens de compra/venda
- 📱 **Interface Responsiva** - Dashboard adaptável para desktop e mobile
- 🔍 **Monitoramento de Ativos** - Acompanhamento detalhado de posições e P&L

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8 ou superior
- Conta ativa na Clear Trading
- Chaves de API configuradas

### Instalação

```bash
# Clone o repositório
git clone https://github.com/rnec/ClearAPI.git
cd ClearAPI

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp clear_api_config.env.example clear_api_config.env
# Edite o arquivo com suas credenciais
```

### Configuração

1. **Configure suas credenciais** no arquivo `clear_api_config.env`:
```env
CLIENT_ID=seu_client_id
ACCESS_TOKEN=seu_access_token
REFRESH_TOKEN=seu_refresh_token
```

2. **Execute os testes de conectividade**:
```bash
python test_connectivity.py
python test_auth.py
```

## 🖥️ Como Usar

### Dashboard Web
```bash
# Inicie o servidor web
python start_web_dashboard.py

# Acesse: http://localhost:5000
```

### API Direta
```python
from ClearAPI.main import ClearAPI

# Inicialize a API
api = ClearAPI()

# Obtenha cotações
quotes = api.get_quotes(['PETR4', 'VALE3'])

# Execute uma ordem
order = api.send_order(
    symbol='PETR4',
    side='buy',
    quantity=100,
    price=25.50
)
```

## 📁 Estrutura do Projeto

```
ClearAPI/
├── ClearAPI/              # Módulo principal da API
│   ├── auth.py           # Sistema de autenticação
│   ├── get_ticker_quote.py # Obtenção de cotações
│   ├── send_order.py     # Execução de ordens
│   ├── websocket_client.py # Cliente WebSocket
│   └── signature.py      # Assinatura de requisições
├── frontend/             # Interface web
│   ├── static/          # CSS e JavaScript
│   └── templates/       # Templates HTML
├── web_app.py           # Aplicação Flask
├── quote_monitor.py     # Monitor de cotações
└── requirements.txt     # Dependências
```

## 📚 Documentação

- [📖 Configuração Detalhada](README_CONFIG.md)
- [🌐 Interface Web](README_WEB_INTERFACE.md)
- [📋 Documentação da API](clear_api_documentation.md)

## 🧪 Testes

```bash
# Teste de conectividade
python test_connectivity.py

# Teste de autenticação
python test_auth.py

# Teste WebSocket
python test_websocket_simple.py
```

## 🔧 Funcionalidades Avançadas

### WebSocket em Tempo Real
- Cotações atualizadas automaticamente
- Monitoramento de posições
- Alertas de preço personalizáveis

### Dashboard Interativo
- Gráficos dinâmicos
- Histórico de operações
- Análise de performance

### Sistema de Ordens
- Ordens a mercado e limitadas
- Stop loss e take profit
- Gerenciamento de risco

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Disclaimer

Este software é fornecido para fins educacionais e de desenvolvimento. O uso em ambiente de produção deve ser feito com cautela e sob sua própria responsabilidade. Trading envolve riscos financeiros significativos.

## 📞 Contato

- **Email**: rnectrade@gmail.com
- **GitHub**: [@rnec](https://github.com/rnec)

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
