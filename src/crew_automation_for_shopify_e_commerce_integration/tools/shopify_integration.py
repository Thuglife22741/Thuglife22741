"""Module for Shopify store integration and sales page creation."""

from .product_data import get_product_data
from .product_management import create_product

def create_sales_page():
    """Create a sales page in Shopify store using product data."""
    # Get product data
    product_data = get_product_data()
    
    # Create product in Shopify
    result = create_product(
        title=product_data['title'],
        description=product_data['description'],
        price=product_data['price'],
        images=product_data['images'],
        variants=product_data['variants'],
        compare_at_price=product_data['compare_at_price']
    )
    
    if result:
        return {
            'success': True,
            'product_id': result['id'],
            'product_title': result['title'],
            'product_handle': result['handle']
        }
    
    return {
        'success': False,
        'error': 'Failed to create product in Shopify'
    }