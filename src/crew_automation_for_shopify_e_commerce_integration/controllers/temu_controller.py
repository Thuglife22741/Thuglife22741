"""Controller for managing Temu product scraping and Shopify integration."""

from flask import Blueprint, request, jsonify
from ..tools.temu_scraper import TemuScraper

app = Blueprint('temu', __name__)

@app.route('/scrape-product', methods=['POST'])
def scrape_temu_product():
    """Endpoint to scrape Temu product and create in Shopify."""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['url', 'keywords', 'store_name']):
            return jsonify({
                'error': 'Missing required fields. Please provide url, keywords, and store_name'
            }), 400
        
        scraper = TemuScraper(
            url=data['url'],
            keywords=data['keywords'],
            store_name=data['store_name']
        )
        
        product = scraper.extract_product_info()
        
        if product:
            return jsonify({
                'message': 'Product successfully created in Shopify',
                'product': product
            }), 201
        
        return jsonify({
            'error': 'Failed to create product'
        }), 500
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500