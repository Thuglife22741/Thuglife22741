"""Configuration module for Shopify API credentials."""

SHOPIFY_CONFIG = {
    'shop_url': 'your-store.myshopify.com',
    'access_token': 'your_access_token',
    'api_version': '2024-01',
    'api_key': 'your_api_key',
    'api_secret': 'your_api_secret'
}

def get_shopify_config():
    """Get Shopify configuration settings."""
    return SHOPIFY_CONFIG