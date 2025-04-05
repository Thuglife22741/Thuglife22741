"""Module for loading and managing API credentials."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Shopify API Credentials
SHOPIFY_ADMIN_TOKEN = os.getenv('SHOPIFY_ADMIN_TOKEN')
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')

# OpenAI API Credentials
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Instagram API Credentials
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID')
INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

def validate_credentials():
    """Validate that all required credentials are present."""
    required_vars = [
        'SHOPIFY_ADMIN_TOKEN',
        'SHOPIFY_API_KEY',
        'SHOPIFY_API_SECRET',
        'SHOPIFY_SHOP_URL',
        'OPENAI_API_KEY',
        'INSTAGRAM_USERNAME',
        'INSTAGRAM_PASSWORD',
        'INSTAGRAM_APP_ID',
        'INSTAGRAM_APP_SECRET',
        'INSTAGRAM_ACCESS_TOKEN'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
    
    return True