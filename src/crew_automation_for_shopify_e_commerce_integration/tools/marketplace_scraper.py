"""Module for scraping product data from various marketplaces and integrating with Shopify."""

import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from .product_management import create_product

class MarketplaceScraper:
    def __init__(self, url, keywords, store_name):
        self.url = url
        self.keywords = keywords
        self.store_name = store_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_product_info(self):
        """Extract product information from marketplace URL."""
        try:
            marketplace = self._detect_marketplace()
            if marketplace == 'temu':
                return self._extract_temu_product()
            elif marketplace == 'aliexpress':
                return self._extract_aliexpress_product()
            elif marketplace == 'amazon':
                return self._extract_amazon_product()
            else:
                raise Exception('Marketplace não suportado')
                
        except Exception as e:
            raise Exception(f"Falha ao extrair dados do produto: {str(e)}")
    
    def _detect_marketplace(self):
        """Detect marketplace from URL."""
        if 'temu.com' in self.url.lower():
            return 'temu'
        elif 'aliexpress.com' in self.url.lower():
            return 'aliexpress'
        elif 'amazon.com' in self.url.lower():
            return 'amazon'
        return 'unknown'
    
    def _extract_temu_product(self):
        """Extract product data from Temu."""
        try:
            encoded_name = re.search(r'br/(.*?)-g-', self.url).group(1)
            product_name = unquote(encoded_name).replace('-', ' ')
            
            image_url = re.search(r'top_gallery_url=(.*?)&', self.url)
            if image_url:
                image_url = unquote(image_url.group(1))
            
            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return self._create_shopify_product(product_name, image_url)
            
        except Exception as e:
            raise Exception(f"Falha ao extrair produto do Temu: {str(e)}")
    
    def _extract_aliexpress_product(self):
        """Extract product data from AliExpress."""
        try:
            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrair dados do script JSON do AliExpress
            scripts = soup.find_all('script')
            for script in scripts:
                if 'window.runParams' in str(script):
                    data = str(script).split('data: ')[1].split(',\n')[0]
                    product_data = json.loads(data)
                    
                    product_name = product_data.get('title', '')
                    image_url = product_data.get('imageUrl', '')
                    
                    return self._create_shopify_product(product_name, image_url)
                    
            raise Exception('Dados do produto não encontrados')
            
        except Exception as e:
            raise Exception(f"Falha ao extrair produto do AliExpress: {str(e)}")
    
    def _extract_amazon_product(self):
        """Extract product data from Amazon."""
        try:
            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            product_name = soup.find('span', {'id': 'productTitle'})
            if product_name:
                product_name = product_name.text.strip()
            
            image_element = soup.find('img', {'id': 'landingImage'})
            image_url = image_element.get('src') if image_element else None
            
            return self._create_shopify_product(product_name, image_url)
            
        except Exception as e:
            raise Exception(f"Falha ao extrair produto da Amazon: {str(e)}")
    
    def _create_shopify_product(self, title, image_url):
        """Create optimized product in Shopify."""
        description = self._generate_seo_description(title)
        
        product_data = {
            'title': title,
            'description': description,
            'price': '99.90',  # Preço competitivo
            'images': [image_url] if image_url else None
        }
        
        return create_product(**product_data)
    
    def _generate_seo_description(self, product_name):
        """Generate SEO optimized description using keywords."""
        description = f"""<h2>{product_name}</h2>
        <p>Descubra nossa exclusiva {self.keywords} na {self.store_name}! 
        Peça única com design moderno e confortável, perfeita para todas as ocasiões.</p>
        
        <h3>Características Principais:</h3>
        <ul>
            <li>Material de alta qualidade</li>
            <li>Design contemporâneo</li>
            <li>Conforto excepcional</li>
            <li>Ideal para uso casual ou social</li>
        </ul>
        
        <h3>Por que escolher nossa {self.keywords}?</h3>
        <p>Oferecemos a melhor relação custo-benefício do mercado, 
        com produtos de qualidade superior e design exclusivo.</p>
        
        <h3>Garantia de Satisfação</h3>
        <p>Sua satisfação é nossa prioridade! Compre com confiança na {self.store_name}.</p>"""
        
        return description