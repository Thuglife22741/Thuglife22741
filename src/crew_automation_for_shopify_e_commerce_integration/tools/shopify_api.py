"""Module for interacting with Shopify API."""

import shopify
from typing import Dict, List, Optional

from ..config.shopify_config import get_shopify_config

def initialize_shopify_session():
    """Initialize Shopify API session with credentials."""
    config = get_shopify_config()
    
    shop_url = f"https://{config['shop_url']}"
    access_token = config['access_token']
    api_version = config['api_version']
    api_key = config['api_key']
    api_secret = config['api_secret']
    
    try:
        # Validate credentials
        if not all([shop_url, access_token, api_key, api_secret]):
            raise Exception('Credenciais da Shopify incompletas. Por favor, verifique as configurações.')
            
        # Initialize session with API credentials
        shopify.Session.setup(api_key=api_key, secret=api_secret)
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)
        
        # Test connection
        shop = shopify.Shop.current()
        if not shop:
            raise Exception('Não foi possível conectar à loja Shopify. Verifique suas credenciais.')
            
        return session
        
    except Exception as e:
        raise Exception(f'Erro ao inicializar sessão Shopify: {str(e)}')


def get_shop_info() -> Dict:
    """Get shop information."""
    initialize_shopify_session()
    shop = shopify.Shop.current()
    return {
        'name': shop.name,
        'email': shop.email,
        'domain': shop.domain,
        'country': shop.country_name
    }

def create_product_from_url(url: str, keywords: str) -> Dict:
    """Create a new product from competitor URL."""
    from .temu_scraper import TemuScraper
    import re
    from urllib.parse import unquote
    
    try:
        initialize_shopify_session()
        
        # Extract image URL from the product URL
        image_url_match = re.search(r'top_gallery_url=(.*?)&', url)
        if image_url_match:
            image_url = unquote(image_url_match.group(1))
        else:
            image_url = None
            
        # Extract product name from URL
        product_name_match = re.search(r'br/(.*?)-g-', url)
        if product_name_match:
            product_name = unquote(product_name_match.group(1)).replace('-', ' ')
        else:
            product_name = keywords
        
        # Create product in Shopify
        product = shopify.Product()
        product.title = product_name.title()
        product.body_html = f"""<h2>Camisa Masculina Premium</h2>
        <p>Apresentamos nossa exclusiva {product_name} na iaseo.com! 
        Uma peça sofisticada e elegante, perfeita para todas as ocasiões.</p>
        
        <h3>🌟 Características Principais:</h3>
        <ul>
            <li>Design Moderno e Elegante</li>
            <li>Tecido de Alta Qualidade</li>
            <li>Conforto Excepcional</li>
            <li>Acabamento Premium</li>
            <li>Durabilidade Garantida</li>
        </ul>
        
        <h3>✨ Diferenciais:</h3>
        <ul>
            <li>Corte Anatômico</li>
            <li>Tecido Respirável</li>
            <li>Fácil de Cuidar</li>
            <li>Versátil para Qualquer Ocasião</li>
            <li>Estilo Atemporal</li>
        </ul>
        
        <h3>💫 Por que Escolher Nossa Camisa?</h3>
        <p>Esta camisa é mais que uma peça de roupa - é uma declaração de estilo e qualidade. 
        Ideal para homens que valorizam conforto e elegância em seu dia a dia.</p>
        
        <h3>✅ Garantia de Qualidade</h3>
        <p>Oferecemos garantia de satisfação total! Cada peça é cuidadosamente inspecionada 
        para garantir a mais alta qualidade. Compre com confiança na iaseo.com.</p>
        
        <h3>🚚 Envio Rápido e Seguro</h3>
        <p>Entregamos seu pedido com todo cuidado e agilidade. Embalagem especial para garantir 
        que sua camisa chegue em perfeitas condições.</p>"""
        
        # Create variant
        variant = shopify.Variant({
            'price': '99.90',
            'compare_at_price': '199.90',
            'inventory_management': 'shopify',
            'inventory_quantity': 100,
            'requires_shipping': True
        })
        product.variants = [variant]
        
        # Add image
        if image_url:
            image = shopify.Image({
                'src': image_url
            })
            product.images = [image]
        
        if product.save():
            return {
                'id': product.id,
                'title': product.title,
                'handle': product.handle,
                'url': f"https://iaseoshopfy.myshopify.com/products/{product.handle}"
            }
        
        raise Exception('Falha ao criar produto na Shopify')
        
    except Exception as e:
        raise Exception(f"Erro ao criar produto: {str(e)}")