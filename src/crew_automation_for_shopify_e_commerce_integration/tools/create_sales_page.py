"""Module for creating sales pages from competitor URLs."""

import os
from dotenv import load_dotenv
from .shopify_api import create_product_from_url
from .shopify_session import initialize_shopify_session

def create_sales_page():
    """Create a sales page from competitor URL."""
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
        result = create_product_from_url(
            title=product_data['title'],
            description=product_data['description'],
            price=product_data['price'],
            compare_at_price=product_data['compare_at_price'],
            images=product_data['images'],
            variants=product_data['variants']
        )
        
        if result:
            print(f"Sales page created successfully! Product ID: {result['id']}")
            print(f"View your product at: https://{shop['domain']}/products/{result['handle']}")
            return result
        else:
            raise Exception("Failed to create sales page")
            
    except Exception as e:
        raise Exception(f"Error creating sales page: {str(e)}")