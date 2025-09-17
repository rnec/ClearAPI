# signature.py
import json
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from config import PRIVATE_RSA_KEY_PATH

def generate_body_signature(body: str | dict) -> str:
    try:
        # Converte o corpo para string, se necessário
        body_string = body if isinstance(body, str) else json.dumps(body)

        # Carrega a chave privada RSA
        with open(PRIVATE_RSA_KEY_PATH, 'rb') as key_file:
                rsa_private_key = load_pem_private_key(key_file.read(), password=None)

        # Gera a assinatura
        signature = rsa_private_key.sign(
            body_string.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # Retorna a assinatura em base64
        return base64.b64encode(signature).decode()
    except Exception as e:
        raise ValueError(f"Erro ao gerar a assinatura: {str(e)}")