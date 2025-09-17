# send_order.py
import requests
import json
from typing import Dict, Any, Literal
from signature import generate_body_signature # Usar exemplo 'Gerar BODY_SIGNATURE'
from auth import get_auth_token # Usar exemplo 'Obter um token de acesso'

# Tipos para os parâmetros da ordem
ModuleType = Literal['Default', 'DayTrade', 'SwingTrade']  # atualmente somente 'DayTrade' está disponível
SideType = Literal['Buy', 'Sell']
TimeInForceType = Literal['Day', 'ImmediateOrCancel', 'FillOrKill']

class SendLimitedOrderRequest:
    """
    Classe que define o formato do corpo da requisição para envio de uma ordem limitada.
    """
    def __init__(
        self,
        module: ModuleType,
        ticker: str,
        side: SideType,
        price: float,
        quantity: int,
        time_in_force: TimeInForceType
    ):
        self.Module = module
        self.Ticker = ticker
        self.Side = side
        self.Price = price
        self.Quantity = quantity
        self.TimeInForce = time_in_force
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'Module': self.Module,
            'Ticker': self.Ticker,
            'Side': self.Side,
            'Price': self.Price,
            'Quantity': self.Quantity,
            'TimeInForce': self.TimeInForce
        }

class SendMarketOrderRequest:
    """
    Classe que define o formato do corpo da requisição para envio de uma ordem a mercado.
    """
    def __init__(
        self,
        module: ModuleType,
        ticker: str,
        side: SideType,
        quantity: int,
        time_in_force: TimeInForceType
    ):
        self.Module = module
        self.Ticker = ticker
        self.Side = side
        self.Quantity = quantity
        self.TimeInForce = time_in_force
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'Module': self.Module,
            'Ticker': self.Ticker,
            'Side': self.Side,
            'Quantity': self.Quantity,
            'TimeInForce': self.TimeInForce
        }

class SendOrderResponse:
    """
    Classe que define o formato da resposta ao enviar uma ordem limitada.
    """
    def __init__(self, order_id: str):
        self.order_id = order_id

class ErrorsResponse:
    """
    Classe que define o formato da resposta de erro.
    """
    def __init__(self, error_response: list):
        self.error_response = error_response

def send_limited_order(
    order_request: SendLimitedOrderRequest
) -> SendOrderResponse:
    """
    Envia uma ordem limitada para a API.
    
    Args:
        order_request: Objeto contendo os dados da ordem limitada.
        access_token: Token de autenticação para a API.
    
    Returns:
        Um objeto contendo a confirmação do envio da ordem.
    
    Raises:
        requests.HTTPError: Erro caso a requisição falhe ou a API retorne um erro.
    """
    url = 'https://variableincome-openapi-simulator.xpi.com.br/api/v1/orders/send/limited'
    body = json.dumps(order_request.to_dict())
    body_signature = generate_body_signature(body)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_auth_token()}',
        'User-Agent': 'Smart-Trader-API Devs-Clear',
        'BODY_SIGNATURE': body_signature
    }

    try:
        response = requests.post(url, headers=headers, data=body)
        
        if not response.ok:
            if response.status_code == 500:
                error_data = response.json()
                error_messages = '; '.join([
                    f'{err['code']} - {err['message']}'
                    for err in error_data.get('errorResponse', [])
                ])
                raise requests.HTTPError(f'Erro interno: {error_messages}')
            
            raise requests.HTTPError(
                f'Erro na requisição: {response.status_code} - {response.reason}'
            )

        data = response.json()
        return SendOrderResponse(data['orderId'])
        
    except requests.exceptions.RequestException as e:
        raise requests.HTTPError(f'Erro ao enviar a ordem limitada: {str(e)}')
    except json.JSONDecodeError as e:
        raise ValueError(f'Erro ao decodificar resposta JSON: {str(e)}')
    except Exception as e:
        raise Exception(f'Erro inesperado: {str(e)}')

def send_market_order(
    order_request: SendMarketOrderRequest
) -> SendOrderResponse:
    """
    Envia uma ordem a mercado para a API.
    
    Args:
        order_request: Objeto contendo os dados da ordem a mercado.
    
    Returns:
        Um objeto contendo a confirmação do envio da ordem.
    
    Raises:
        requests.HTTPError: Erro caso a requisição falhe ou a API retorne um erro.
    """
    url = 'https://variableincome-openapi-simulator.xpi.com.br/api/v1/orders/send/market'
    body = json.dumps(order_request.to_dict())
    body_signature = generate_body_signature(body)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_auth_token()}',
        'User-Agent': 'Smart-Trader-API Devs-Clear',
        'BODY_SIGNATURE': body_signature
    }

    try:
        response = requests.post(url, headers=headers, data=body)
        
        if not response.ok:
            if response.status_code == 500:
                error_data = response.json()
                error_messages = '; '.join([
                    f'{err['code']} - {err['message']}'
                    for err in error_data.get('errorResponse', [])
                ])
                raise requests.HTTPError(f'Erro interno: {error_messages}')
            
            raise requests.HTTPError(
                f'Erro na requisição: {response.status_code} - {response.reason}'
            )

        data = response.json()
        return SendOrderResponse(data['orderId'])
        
    except requests.exceptions.RequestException as e:
        raise requests.HTTPError(f'Erro ao enviar a ordem a mercado: {str(e)}')
    except json.JSONDecodeError as e:
        raise ValueError(f'Erro ao decodificar resposta JSON: {str(e)}')
    except Exception as e:
        raise Exception(f'Erro inesperado: {str(e)}')