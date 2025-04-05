"""Module for managing Shopify products and collections."""

import shopify
from .shopify_api import initialize_shopify_session

def create_product(title, description, price, images=None, variants=None, compare_at_price=None):
    """Create a new product in Shopify store."""
    session = initialize_shopify_session()
    try:
        new_product = shopify.Product()
        new_product.title = title
        new_product.body_html = description
        new_product.vendor = shopify.Shop.current().name
        new_product.product_type = 'Cadernos Personalizados'
        
        # Create variants
        if variants:
            product_variants = []
            for variant_data in variants:
                variant = shopify.Variant({
                    'title': variant_data['title'],
                    'price': variant_data['price'],
                    'inventory_management': 'shopify',
                    'inventory_quantity': variant_data['inventory_quantity'],
                    'compare_at_price': compare_at_price
                })
                product_variants.append(variant)
            new_product.variants = product_variants
        else:
            # Create default variant with price
            variant = shopify.Variant({
                'price': price,
                'inventory_management': 'shopify',
                'inventory_quantity': 1,
                'compare_at_price': compare_at_price
            })
            new_product.variants = [variant]
        
        # Add images if provided
        if images:
            for image_url in images:
                image = shopify.Image({
                    'src': image_url
                })
                new_product.images.append(image)
        
        if new_product.save():
            return {
                'id': new_product.id,
                'title': new_product.title,
                'handle': new_product.handle
            }
        return None
    except Exception as e:
        raise Exception(f"Failed to create product: {str(e)}")

def get_all_products():
    """Get all products from the Shopify store."""
    session = initialize_shopify_session()
    try:
        products = shopify.Product.find()
        return [{
            'id': product.id,
            'title': product.title,
            'handle': product.handle,
            'price': product.variants[0].price if product.variants else None,
            'image_url': product.images[0].src if product.images else None
        } for product in products]
    except Exception as e:
        raise Exception(f"Failed to fetch products: {str(e)}")

def update_product(product_id, **kwargs):
    """Update an existing product in Shopify store."""
    session = initialize_shopify_session()
    try:
        product = shopify.Product.find(product_id)
        for key, value in kwargs.items():
            setattr(product, key, value)
        
        if product.save():
            return {
                'id': product.id,
                'title': product.title,
                'handle': product.handle
            }
        return None
    except Exception as e:
        raise Exception(f"Failed to update product: {str(e)}")

def delete_product(product_id):
    """Delete a product from Shopify store."""
    session = initialize_shopify_session()
    try:
        product = shopify.Product.find(product_id)
        return product.destroy()
    except Exception as e:
        raise Exception(f"Failed to delete product: {str(e)}")