"""Controller for managing sales page and product operations."""

from flask import Blueprint, render_template, jsonify, request
from crew_automation_for_shopify_e_commerce_integration.tools.product_management import get_all_products, create_product, update_product, delete_product
from crew_automation_for_shopify_e_commerce_integration.tools.shopify_api import get_shop_info

app = Blueprint('sales', __name__, template_folder='../templates')

@app.route('/')
def index():
    """Render the sales page with products."""
    try:
        # Get shop information
        shop = get_shop_info()
        
        # Get all products
        products = get_all_products()
        
        return render_template('sales_page.html', shop=shop, products=products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/from-url', methods=['POST'])
def create_from_url():
    """Create a new product from competitor URL."""
    try:
        data = request.json
        if not data.get('url') or not data.get('keywords'):
            return jsonify({'error': 'URL e palavras-chave são obrigatórias'}), 400
            
        from ..tools.shopify_api import create_product_from_url
        result = create_product_from_url(
            url=data['url'],
            keywords=data['keywords']
        )
        
        return jsonify({
            'message': 'Produto criado com sucesso',
            'product': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product to the store."""
    try:
        data = request.json
        result = create_product(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            images=data.get('images')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product_route(product_id):
    """Update an existing product."""
    try:
        data = request.json
        result = update_product(product_id, **data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    """Delete a product from the store."""
    try:
        result = delete_product(product_id)
        return jsonify({'success': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)