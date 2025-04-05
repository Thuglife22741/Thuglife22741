"""Script para automatizar postagens no Instagram."""

from .instagram_api import create_instagram_post_from_product
from ..config.credentials import validate_credentials
import json
import time

def validate_product_data(product_data):
    """Validar dados do produto antes da postagem."""
    required_fields = ['title', 'price', 'url', 'image_url']
    missing_fields = [field for field in required_fields if not product_data.get(field)]
    
    if missing_fields:
        raise ValueError(f"Dados do produto incompletos. Campos faltando: {', '.join(missing_fields)}")
    
    return True

def post_product_to_instagram(product_data, max_retries=3):
    """Postar produto no Instagram com validação e tratamento de erros."""
    try:
        # Validar credenciais
        validate_credentials()
        
        # Validar dados do produto
        validate_product_data(product_data)
        
        # Tentar fazer a postagem
        result = create_instagram_post_from_product(product_data)
        
        return {
            'success': True,
            'message': 'Post criado com sucesso no Instagram',
            'result': result
        }
        
    except ValueError as e:
        return {
            'success': False,
            'message': str(e),
            'error_type': 'validation_error'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erro ao criar post: {str(e)}',
            'error_type': 'system_error'
        }

def batch_post_to_instagram(products, delay_between_posts=300):
    """Postar múltiplos produtos no Instagram com intervalo entre postagens."""
    results = []
    
    for product in products:
        result = post_product_to_instagram(product)
        results.append(result)
        
        if not result['success']:
            print(f"Erro ao postar produto {product.get('title', 'Unknown')}: {result['message']}")
        else:
            print(f"Produto {product.get('title', 'Unknown')} postado com sucesso!")
        
        # Aguardar entre postagens para evitar rate limiting
        if len(products) > 1:
            time.sleep(delay_between_posts)
    
    return results