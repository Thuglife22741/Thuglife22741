"""Controller for managing sales page creation in Shopify."""

from flask import Blueprint, jsonify
from ..tools.shopify_integration import create_sales_page

sales_page_bp = Blueprint('sales_page', __name__)

@sales_page_bp.route('/api/create-sales-page', methods=['POST'])
def create_shopify_sales_page():
    """Create a sales page in Shopify store."""
    try:
        result = create_sales_page()
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'message': 'Página de vendas criada com sucesso!',
                'data': {
                    'product_id': result['product_id'],
                    'product_title': result['product_title'],
                    'product_url': f'https://sua-loja.myshopify.com/products/{result["product_handle"]}'
                }
            }), 200
        
        return jsonify({
            'status': 'error',
            'message': result['error']
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao criar página de vendas: {str(e)}'
        }), 500