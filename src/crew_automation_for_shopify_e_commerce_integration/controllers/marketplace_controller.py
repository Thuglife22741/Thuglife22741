"""Controller for managing marketplace product scraping and Shopify integration."""

from flask import Blueprint, request, jsonify
from ..tools.marketplace_scraper import MarketplaceScraper

app = Blueprint('marketplace', __name__)

@app.route('/scrape-product', methods=['POST'])
def scrape_marketplace_product():
    """Endpoint to scrape product from any supported marketplace and create in Shopify."""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['url', 'keywords', 'store_name']):
            return jsonify({
                'error': 'Campos obrigatórios ausentes. Por favor, forneça url, keywords e store_name'
            }), 400
        
        scraper = MarketplaceScraper(
            url=data['url'],
            keywords=data['keywords'],
            store_name=data['store_name']
        )
        
        product = scraper.extract_product_info()
        
        if product:
            return jsonify({
                'message': 'Produto criado com sucesso na Shopify',
                'product': product
            }), 201
        
        return jsonify({
            'error': 'Falha ao criar produto'
        }), 500
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500