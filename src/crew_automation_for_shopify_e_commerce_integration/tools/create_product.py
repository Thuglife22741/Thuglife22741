"""Module for creating products in Shopify from competitor URLs."""

import os
from dotenv import load_dotenv
from .shopify_api import create_product_from_url
from .shopify_session import initialize_shopify_session

def create_product_page():
    """Create a product page from competitor URL."""
    try:
        # Initialize Shopify session
        initialize_shopify_session()
        
        # Load environment variables
        load_dotenv()
        
        # Get competitor URL and keywords from environment
        url = os.getenv('CONCORRENTE_URL')
        keywords = os.getenv('PALAVRAS_CHAVE')
        
        if not url or not keywords:
            raise ValueError('URL do concorrente ou palavras-chave não encontradas no arquivo .env')
        
        # Create product in Shopify
        result = create_product_from_url(url, keywords)
        
        if result:
            print(f"Página de produto criada com sucesso! ID do produto: {result['id']}")
            print(f"Visualize seu produto em: {result['url']}")
            return result
        else:
            raise Exception("Falha ao criar página do produto")
            
    except Exception as e:
        print(f'Erro ao criar página do produto: {str(e)}')
        raise

if __name__ == '__main__':
    create_product_page()