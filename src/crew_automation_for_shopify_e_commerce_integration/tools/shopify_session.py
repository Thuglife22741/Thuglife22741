"""Module for managing Shopify API session."""

import shopify
from ..config.shopify_config import get_shopify_config

def initialize_shopify_session():
    """Initialize Shopify API session with credentials."""
    config = get_shopify_config()
    
    shop_url = f"https://{config['shop_url']}"
    access_token = config['access_token']
    api_version = config['api_version']
    
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    
    return session