/**
 * Clear Trading Dashboard - Frontend JavaScript
 * Gerencia WebSocket, interface e dados em tempo real
 */

class TradingDashboard {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.isConnected = false;
        this.subscribedTickers = new Set();
        this.quotesData = new Map();
        this.updateCount = 0;
        
        this.initializeElements();
        this.attachEventListeners();
        this.updateTime();
        this.connectWebSocket();
        
        // Atualiza o tempo a cada segundo
        setInterval(() => this.updateTime(), 1000);
    }

    initializeElements() {
        // Elementos do DOM
        this.elements = {
            tickerInput: document.getElementById('ticker-input'),
            addTickerBtn: document.getElementById('add-ticker-btn'),
            activeTickersCount: document.getElementById('active-tickers'),
            updatesCount: document.getElementById('updates-count'),
            activeTickersList: document.getElementById('active-tickers-list'),
            quotesTableBody: document.getElementById('quotes-table-body'),
            noDataRow: document.getElementById('no-data-row'),
            statusIndicator: document.getElementById('status-indicator'),
            statusText: document.getElementById('status-text'),
            currentTime: document.getElementById('current-time'),
            toastContainer: document.getElementById('toast-container'),
            loadingOverlay: document.getElementById('loading-overlay'),
            quickFilters: document.querySelectorAll('.quick-filter')
        };
    }

    attachEventListeners() {
        // Adicionar ticker
        this.elements.addTickerBtn.addEventListener('click', () => this.addTicker());
        this.elements.tickerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addTicker();
            }
        });

        // Filtros rápidos
        this.elements.quickFilters.forEach(filter => {
            filter.addEventListener('click', () => {
                const filterType = filter.dataset.filter;
                this.applyQuickFilter(filterType);
            });
        });

        // Auto-uppercase no input
        this.elements.tickerInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase();
        });
    }

    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        this.elements.currentTime.textContent = timeString;
    }

    connectWebSocket() {
        try {
            this.showLoading(true);
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                console.log('WebSocket conectado');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.updateConnectionStatus(true);
                this.showLoading(false);
                this.showToast('Conectado ao servidor', 'success');
                
                // Solicita lista de tickers já subscritos
                this.sendMessage({
                    type: 'get_subscribed'
                });
            };

            this.ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    this.handleMessage(message);
                } catch (error) {
                    console.error('Erro ao processar mensagem:', error);
                }
            };

            this.ws.onclose = () => {
                console.log('WebSocket desconectado');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                this.showLoading(false);
                this.attemptReconnect();
            };

            this.ws.onerror = (error) => {
                console.error('Erro no WebSocket:', error);
                this.showToast('Erro de conexão', 'error');
            };

        } catch (error) {
            console.error('Erro ao conectar WebSocket:', error);
            this.showToast('Falha na conexão', 'error');
            this.showLoading(false);
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            this.showToast(`Tentando reconectar... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`, 'warning');
            
            setTimeout(() => {
                this.connectWebSocket();
            }, this.reconnectDelay * this.reconnectAttempts);
        } else {
            this.showToast('Falha na reconexão. Recarregue a página.', 'error');
        }
    }

    sendMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            this.showToast('WebSocket não conectado', 'error');
        }
    }

    handleMessage(message) {
        switch (message.type) {
            case 'quote_update':
                this.handleQuoteUpdate(message.data);
                break;
            case 'subscription_confirmed':
                this.handleSubscriptionConfirmed(message.ticker);
                break;
            case 'unsubscription_confirmed':
                this.handleUnsubscriptionConfirmed(message.ticker);
                break;
            case 'subscribed_tickers':
                this.handleSubscribedTickers(message.tickers);
                break;
            default:
                console.log('Mensagem não reconhecida:', message);
        }
    }

    handleQuoteUpdate(data) {
        this.quotesData.set(data.ticker, data);
        this.updateCount++;
        this.updateQuoteRow(data);
        this.updateStatistics();
        
        // Efeito visual de atualização
        const row = document.getElementById(`row-${data.ticker}`);
        if (row) {
            row.classList.add('bg-blue-50');
            setTimeout(() => row.classList.remove('bg-blue-50'), 500);
        }
    }

    handleSubscriptionConfirmed(ticker) {
        this.subscribedTickers.add(ticker);
        this.updateActiveTickersList();
        this.updateStatistics();
        this.showToast(`${ticker} adicionado com sucesso`, 'success');
    }

    handleUnsubscriptionConfirmed(ticker) {
        this.subscribedTickers.delete(ticker);
        this.quotesData.delete(ticker);
        this.removeQuoteRow(ticker);
        this.updateActiveTickersList();
        this.updateStatistics();
        this.showToast(`${ticker} removido`, 'info');
    }

    handleSubscribedTickers(tickers) {
        this.subscribedTickers = new Set(tickers);
        this.updateActiveTickersList();
        this.updateStatistics();
    }

    addTicker() {
        const ticker = this.elements.tickerInput.value.trim().toUpperCase();
        
        if (!ticker) {
            this.showToast('Digite um ticker válido', 'warning');
            return;
        }

        if (this.subscribedTickers.has(ticker)) {
            this.showToast(`${ticker} já está sendo monitorado`, 'warning');
            return;
        }

        // Envia solicitação de subscrição
        this.sendMessage({
            type: 'subscribe',
            ticker: ticker
        });

        // Limpa o input
        this.elements.tickerInput.value = '';
    }

    removeTicker(ticker) {
        this.sendMessage({
            type: 'unsubscribe',
            ticker: ticker
        });
    }

    async sendOrder(ticker, side) {
        const quantityInput = document.getElementById(`quantity-${ticker}`);
        const quantity = parseInt(quantityInput.value);
        
        // Validação de quantidade
        if (!quantity || quantity <= 0) {
            this.showToast('Quantidade deve ser maior que zero', 'warning');
            quantityInput.classList.add('quantity-error');
            setTimeout(() => quantityInput.classList.remove('quantity-error'), 2000);
            return;
        }

        // Remove classes de erro anteriores
        quantityInput.classList.remove('quantity-error');
        quantityInput.classList.add('quantity-success');
        setTimeout(() => quantityInput.classList.remove('quantity-success'), 1000);

        // Encontra os botões
        const buyBtn = document.querySelector(`button[onclick="dashboard.sendOrder('${ticker}', 'Buy')"]`);
        const sellBtn = document.querySelector(`button[onclick="dashboard.sendOrder('${ticker}', 'Sell')"]`);
        const activeBtn = side === 'Buy' ? buyBtn : sellBtn;
        
        // Desabilita botões e adiciona animação de carregamento
        if (buyBtn) {
            buyBtn.disabled = true;
            buyBtn.classList.add('opacity-50');
        }
        if (sellBtn) {
            sellBtn.disabled = true;
            sellBtn.classList.add('opacity-50');
        }
        if (activeBtn) {
            activeBtn.classList.add('loading-order');
        }

        try {
            const response = await fetch('/api/order/market', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ticker: ticker,
                    side: side,
                    quantity: quantity
                })
            });

            const result = await response.json();

            if (result.success) {
                this.showOrderToast(result.data.message, 'success');
                // Reset quantity to 1 after successful order
                quantityInput.value = '1';
                
                // Efeito visual de sucesso - sem piscar
                if (activeBtn) {
                    activeBtn.style.transform = 'scale(1.05)';
                    activeBtn.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.5)';
                    setTimeout(() => {
                        activeBtn.style.transform = '';
                        activeBtn.style.boxShadow = '';
                    }, 500);
                }
            } else {
                this.showOrderToast(`Erro: ${result.error}`, 'error');
            }

        } catch (error) {
            this.showOrderToast(`Erro de conexão: ${error.message}`, 'error');
        } finally {
            // Reabilita botões e remove animações
            if (buyBtn) {
                buyBtn.disabled = false;
                buyBtn.classList.remove('opacity-50');
            }
            if (sellBtn) {
                sellBtn.disabled = false;
                sellBtn.classList.remove('opacity-50');
            }
            if (activeBtn) {
                activeBtn.classList.remove('loading-order');
            }
        }
    }

    showOrderToast(message, type = 'info') {
        const toast = document.createElement('div');
        const colors = {
            success: 'bg-green-500 order-toast',
            error: 'bg-red-500 order-toast error',
            warning: 'bg-yellow-500',
            info: 'bg-blue-500'
        };

        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        toast.className = `${colors[type]} text-white px-4 py-3 rounded-lg shadow-lg flex items-center space-x-2 transform transition-all duration-300 translate-x-full`;
        toast.innerHTML = `
            <i class="fas ${icons[type]}"></i>
            <span>${message}</span>
            ${type === 'success' ? '<i class="fas fa-coins ml-2 text-yellow-200"></i>' : ''}
        `;

        this.elements.toastContainer.appendChild(toast);

        // Animação de entrada
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);

        // Remove após 4 segundos (mais tempo para ordens)
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }

    applyQuickFilter(filterType) {
        const commonTickers = {
            'WIN': ['WINV25', 'WINH25', 'WINJ25'],
            'WDO': ['WDOV25', 'WDOH25', 'WDOJ25'],
            'ALL': ['WINV25', 'WDOV25', 'PETRV25', 'VALEV25']
        };

        if (commonTickers[filterType]) {
            commonTickers[filterType].forEach(ticker => {
                if (!this.subscribedTickers.has(ticker)) {
                    this.sendMessage({
                        type: 'subscribe',
                        ticker: ticker
                    });
                }
            });
        }
    }

    updateActiveTickersList() {
        const container = this.elements.activeTickersList;
        
        if (this.subscribedTickers.size === 0) {
            container.innerHTML = '<div class="text-gray-500 italic">Nenhum ticker ativo. Adicione um ticker acima para começar.</div>';
            return;
        }

        container.innerHTML = Array.from(this.subscribedTickers).map(ticker => `
            <div class="inline-flex items-center bg-trading-blue text-white px-3 py-1 rounded-full text-sm">
                <span class="mr-2">${ticker}</span>
                <button 
                    onclick="dashboard.removeTicker('${ticker}')" 
                    class="hover:bg-blue-600 rounded-full p-1 transition-colors"
                    title="Remover ${ticker}"
                >
                    <i class="fas fa-times text-xs"></i>
                </button>
            </div>
        `).join('');
    }

    updateQuoteRow(data) {
        let row = document.getElementById(`row-${data.ticker}`);
        
        if (!row) {
            // Criar nova linha
            row = document.createElement('tr');
            row.id = `row-${data.ticker}`;
            row.className = 'hover:bg-gray-50 transition-colors';
            this.elements.quotesTableBody.appendChild(row);
            
            // Remove a linha "sem dados" se existir
            if (this.elements.noDataRow) {
                this.elements.noDataRow.style.display = 'none';
            }
        }

        // Calcula variação e cor
        const change = data.change || 0;
        const changePercent = data.changePercent || 0;
        const changeColor = change >= 0 ? 'text-trading-green' : 'text-trading-red';
        const changeIcon = change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';

        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="w-2 h-2 bg-trading-green rounded-full mr-3 animate-pulse"></div>
                    <div class="text-sm font-medium text-gray-900">${data.ticker}</div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">R$ ${data.lastPrice.toFixed(4)}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center ${changeColor}">
                    <i class="fas ${changeIcon} mr-1 text-xs"></i>
                    <span class="text-sm font-medium">
                        ${change >= 0 ? '+' : ''}${change.toFixed(2)} (${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%)
                    </span>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${data.volume ? data.volume.toLocaleString() : '-'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${data.timestamp}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <input 
                    type="number" 
                    id="quantity-${data.ticker}" 
                    placeholder="Qtd" 
                    min="1" 
                    value="1"
                    class="quantity-input w-16 px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-trading-blue focus:border-transparent"
                >
            </td>
            <td class="px-6 py-4 whitespace-nowrap operations-section">
                <div class="flex space-x-2">
                    <button 
                        onclick="dashboard.sendOrder('${data.ticker}', 'Buy')"
                        class="order-button buy-button px-3 py-1 text-white text-xs rounded flex items-center space-x-1"
                        title="Comprar ${data.ticker}"
                    >
                        <i class="fas fa-arrow-up text-xs"></i>
                        <span>Comprar</span>
                    </button>
                    <button 
                        onclick="dashboard.sendOrder('${data.ticker}', 'Sell')"
                        class="order-button sell-button px-3 py-1 text-white text-xs rounded flex items-center space-x-1"
                        title="Vender ${data.ticker}"
                    >
                        <i class="fas fa-arrow-down text-xs"></i>
                        <span>Vender</span>
                    </button>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <button 
                    onclick="dashboard.removeTicker('${data.ticker}')"
                    class="text-red-600 hover:text-red-800 transition-colors"
                    title="Remover ${data.ticker}"
                >
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
    }

    removeQuoteRow(ticker) {
        const row = document.getElementById(`row-${ticker}`);
        if (row) {
            row.remove();
        }

        // Mostra mensagem "sem dados" se não há mais linhas
        if (this.elements.quotesTableBody.children.length === 0 || 
            (this.elements.quotesTableBody.children.length === 1 && this.elements.noDataRow)) {
            if (this.elements.noDataRow) {
                this.elements.noDataRow.style.display = '';
            }
        }
    }

    updateStatistics() {
        this.elements.activeTickersCount.textContent = this.subscribedTickers.size;
        this.elements.updatesCount.textContent = this.updateCount;
    }

    updateConnectionStatus(connected) {
        if (connected) {
            this.elements.statusIndicator.className = 'w-3 h-3 rounded-full bg-green-500 animate-pulse';
            this.elements.statusText.textContent = 'Conectado';
        } else {
            this.elements.statusIndicator.className = 'w-3 h-3 rounded-full bg-red-500';
            this.elements.statusText.textContent = 'Desconectado';
        }
    }

    showLoading(show) {
        this.elements.loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500',
            info: 'bg-blue-500'
        };

        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        toast.className = `${colors[type]} text-white px-4 py-3 rounded-lg shadow-lg flex items-center space-x-2 transform transition-all duration-300 translate-x-full`;
        toast.innerHTML = `
            <i class="fas ${icons[type]}"></i>
            <span>${message}</span>
        `;

        this.elements.toastContainer.appendChild(toast);

        // Animação de entrada
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);

        // Remove após 3 segundos
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
}

// Inicializa o dashboard quando a página carrega
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new TradingDashboard();
});

// Expõe o dashboard globalmente para uso nos event handlers inline
window.dashboard = dashboard;
