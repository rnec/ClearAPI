# Clear Trading Dashboard - Interface Web

## 📋 Visão Geral

Interface web moderna para monitoramento de cotações em tempo real, desenvolvida com FastAPI + HTML5 + Tailwind CSS. Integra com a ClearAPI para receber dados de mercado via WebSocket.

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   ClearAPI      │    │   FastAPI        │    │   Frontend      │
│   WebSocket     │───▶│   Bridge         │───▶│   Dashboard     │
│   (Mercado)     │    │   + WebSocket    │    │   (Browser)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Estrutura do Projeto

```
ClearAPI/
├── web_app.py                 # Aplicação FastAPI principal
├── requirements.txt           # Dependências Python
├── frontend/
│   ├── templates/
│   │   └── dashboard.html     # Página principal
│   └── static/
│       ├── css/
│       │   └── dashboard.css  # Estilos customizados
│       └── js/
│           └── dashboard.js   # Lógica do frontend
└── ClearAPI/                  # Seu código existente
    ├── auth.py
    ├── websocket_client.py
    ├── get_ticker_quote.py
    └── ...
```

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Ambiente

Certifique-se que o arquivo `clear_api_config.env` está configurado corretamente com suas credenciais da ClearAPI.

### 3. Executar a Aplicação

```bash
python web_app.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn web_app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Acessar o Dashboard

Abra seu navegador e acesse: [http://localhost:8000](http://localhost:8000)

## 🎯 Funcionalidades

### ✅ Implementadas

- **Dashboard em Tempo Real**: Interface moderna com dados atualizados via WebSocket
- **Gerenciamento de Tickers**: Adicionar/remover tickers para monitoramento
- **Tabela de Cotações**: Visualização organizada dos dados de mercado
- **Filtros Rápidos**: Botões para adicionar grupos de tickers comuns
- **Status de Conexão**: Indicador visual do status da conexão
- **Notificações Toast**: Feedback visual para ações do usuário
- **Design Responsivo**: Interface adaptada para desktop e mobile
- **Reconexão Automática**: Tenta reconectar automaticamente em caso de perda de conexão

### 📊 Dados Exibidos

- Ticker do ativo
- Última cotação
- Variação (valor e percentual)
- Bid/Ask
- Volume
- Timestamp da última atualização
- Ações (remover ticker)

### 🎨 Interface

- **Framework CSS**: Tailwind CSS para design moderno
- **Ícones**: Font Awesome
- **Cores**: Esquema de cores específico para trading (verde/vermelho)
- **Animações**: Transições suaves e feedback visual
- **Responsividade**: Adaptado para diferentes tamanhos de tela

## 🔧 Configuração Avançada

### Personalizar Porta

```python
# No final do web_app.py
uvicorn.run(app, host="0.0.0.0", port=8080)  # Altere a porta aqui
```

### Adicionar Novos Tickers nos Filtros Rápidos

Edite o arquivo `frontend/static/js/dashboard.js`, método `applyQuickFilter`:

```javascript
const commonTickers = {
    'WIN': ['WINV25', 'WINH25', 'WINJ25'],
    'WDO': ['WDOV25', 'WDOH25', 'WDOJ25'],
    'PETR': ['PETRV25', 'PETRH25'],  // Adicione novos grupos aqui
    'ALL': ['WINV25', 'WDOV25', 'PETRV25', 'VALEV25']
};
```

### Personalizar Estilos

Edite `frontend/static/css/dashboard.css` para personalizar cores, animações e layout.

## 🔍 API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Conexão WebSocket para dados em tempo real

### REST API
- `GET /` - Dashboard principal
- `GET /api/quote/{ticker}` - Obter cotação de um ticker específico

## 🐛 Solução de Problemas

### Erro de Conexão com ClearAPI
1. Verifique se as credenciais no `clear_api_config.env` estão corretas
2. Teste a conectividade com `python test_connectivity.py`
3. Verifique se não há firewall bloqueando a conexão

### Interface não carrega
1. Verifique se o FastAPI está rodando na porta correta
2. Verifique os logs no console do navegador (F12)
3. Certifique-se que os arquivos estáticos estão na pasta correta

### WebSocket não conecta
1. Verifique se há proxy/firewall bloqueando WebSockets
2. Teste com `ws://` ao invés de `wss://` em desenvolvimento
3. Verifique os logs do servidor FastAPI

## 🚀 Próximos Passos (Roadmap)

### Funcionalidades Planejadas

- [ ] **Gráficos em Tempo Real**: Integração com Chart.js ou TradingView
- [ ] **Alertas de Preço**: Configurar alertas para níveis de preço
- [ ] **Histórico de Dados**: Armazenar e visualizar dados históricos
- [ ] **Múltiplas Páginas**: Dashboard, configurações, relatórios
- [ ] **Autenticação**: Sistema de login para múltiplos usuários
- [ ] **API REST Completa**: CRUD para configurações e dados
- [ ] **Temas**: Modo escuro/claro
- [ ] **Export de Dados**: CSV, Excel, PDF
- [ ] **Integração com Ordens**: Interface para envio de ordens
- [ ] **WebSocket Rooms**: Diferentes salas para diferentes usuários

### Melhorias Técnicas

- [ ] **Testes Automatizados**: Unit tests e integration tests
- [ ] **Docker**: Containerização da aplicação
- [ ] **CI/CD**: Pipeline de deploy automatizado
- [ ] **Monitoramento**: Logs estruturados e métricas
- [ ] **Cache**: Redis para cache de dados
- [ ] **Database**: PostgreSQL para persistência
- [ ] **Segurança**: HTTPS, rate limiting, validação

## 📝 Licença

Este projeto é parte do sistema ClearAPI e segue a mesma licença do projeto principal.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

**Desenvolvido com ❤️ para traders brasileiros**
