"""Module for scraping Temu product data and integrating with Shopify."""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from .product_management import create_product

class TemuScraper:
    def __init__(self, url, keywords, store_name):
        self.url = url
        self.keywords = keywords
        self.store_name = store_name
        
    def extract_product_info(self):
        """Extract product information from Temu URL."""
        try:
            # Decode URL-encoded product name from URL
            encoded_name = re.search(r'br/(.*?)-g-', self.url).group(1)
            product_name = unquote(encoded_name).replace('-', ' ')
            
            # Get product image URL from URL parameters
            image_url = re.search(r'top_gallery_url=(.*?)&', self.url)
            if image_url:
                image_url = unquote(image_url.group(1))
            
            # Make request to get product page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract product details
            description = self._generate_seo_description(product_name)
            
            # Create optimized product in Shopify
            product_data = {
                'title': product_name,
                'description': description,
                'price': '99.90',  # Set competitive price
                'images': [image_url] if image_url else None
            }
            
            return create_product(**product_data)
            
        except Exception as e:
            raise Exception(f"Failed to scrape Temu product: {str(e)}")
    
    def _generate_seo_description(self, product_name):
        """Generate SEO optimized description using keywords."""
        description = f"""<h2>Conjunto de Presente Premium {product_name}</h2>
        <p>Apresentamos nosso exclusivo {self.keywords} na {self.store_name}! 
        Um conjunto sofisticado e elegante, perfeito para presentear alguém especial ou para uso próprio.</p>
        
        <h3>🎁 O Que Inclui Este Conjunto Especial:</h3>
        <ul>
            <li>Caderno A5 Personalizável de Alta Qualidade</li>
            <li>Caneta Elegante com Design Premium</li>
            <li>Cartuchos Recarregáveis para Maior Durabilidade</li>
            <li>Caixa de Presente Luxuosa em Vermelho</li>
            <li>Papel Premium para uma Experiência de Escrita Excepcional</li>
        </ul>
        
        <h3>✨ Características Exclusivas:</h3>
        <ul>
            <li>Design Sofisticado e Contemporâneo</li>
            <li>Material Premium Durável</li>
            <li>Personalização Disponível</li>
            <li>Ideal para Ocasiões Especiais</li>
            <li>Perfeito para Uso Profissional ou Pessoal</li>
        </ul>
        
        <h3>💝 Por que Escolher Nosso {self.keywords}?</h3>
        <p>Este conjunto é mais que um simples caderno - é uma experiência completa de escrita e organização. 
        Ideal para profissionais, estudantes ou qualquer pessoa que aprecie produtos de papelaria de alta qualidade.</p>
        
        <h3>✅ Garantia de Qualidade</h3>
        <p>Oferecemos garantia de satisfação total! Cada conjunto é cuidadosamente montado e verificado para garantir 
        a mais alta qualidade. Compre com confiança na {self.store_name}.</p>
        
        <h3>🚚 Envio Rápido e Seguro</h3>
        <p>Entregamos seu pedido com todo cuidado e agilidade. Embalagem especial para garantir que seu conjunto 
        chegue em perfeitas condições.</p>"""
        
        return description