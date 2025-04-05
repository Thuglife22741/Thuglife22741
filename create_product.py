import os
from dotenv import load_dotenv
import shopify
from crew_automation_for_shopify_e_commerce_integration.config.shopify_config import get_shopify_config

def initialize_shopify():
    config = get_shopify_config()
    shop_url = f"https://{config['shop_url']}"
    access_token = config['access_token']
    api_version = config['api_version']
    api_key = config['api_key']
    api_secret = config['api_secret']
    
    shopify.Session.setup(api_key=api_key, secret=api_secret)
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    return session

from crew_automation_for_shopify_e_commerce_integration.tools.instagram_api import create_instagram_post_from_product

def create_product():
    try:
        # Inicializar sessão Shopify
        initialize_shopify()
        
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Obter URL e palavras-chave
        url = os.getenv('CONCORRENTE_URL')
        keywords = os.getenv('PALAVRAS_CHAVE')
        
        # Criar produto
        product = shopify.Product()
        product.title = keywords.title()
        product.body_html = f"""<h2>Camisa Masculina Premium</h2>
        <p>Apresentamos nossa exclusiva {keywords} na iaseo.com! 
        Uma peça sofisticada e elegante, perfeita para todas as ocasiões.</p>
        
        <h3>🌟 Características Principais:</h3>
        <ul>
            <li>Design Moderno e Elegante</li>
            <li>Tecido de Alta Qualidade</li>
            <li>Conforto Excepcional</li>
            <li>Acabamento Premium</li>
            <li>Durabilidade Garantida</li>
        </ul>
        
        <h3>✨ Diferenciais:</h3>
        <ul>
            <li>Corte Anatômico</li>
            <li>Tecido Respirável</li>
            <li>Fácil de Cuidar</li>
            <li>Versátil para Qualquer Ocasião</li>
            <li>Estilo Atemporal</li>
        </ul>
        
        <h3>💫 Por que Escolher Nossa Camisa?</h3>
        <p>Esta camisa é mais que uma peça de roupa - é uma declaração de estilo e qualidade. 
        Ideal para homens que valorizam conforto e elegância em seu dia a dia.</p>
        
        <h3>✅ Garantia de Qualidade</h3>
        <p>Oferecemos garantia de satisfação total! Cada peça é cuidadosamente inspecionada 
        para garantir a mais alta qualidade. Compre com confiança na iaseo.com.</p>
        
        <h3>🚚 Envio Rápido e Seguro</h3>
        <p>Entregamos seu pedido com todo cuidado e agilidade. Embalagem especial para garantir 
        que sua camisa chegue em perfeitas condições.</p>"""
        
        # Criar variante
        variant = shopify.Variant({
            'price': '99.90',
            'compare_at_price': '199.90',
            'inventory_management': 'shopify',
            'inventory_quantity': 100,
            'requires_shipping': True
        })
        product.variants = [variant]
        
        # Adicionar imagem
        if 'top_gallery_url=' in url:
            image_url = url.split('top_gallery_url=')[1].split('&')[0]
            image = shopify.Image({'src': image_url})
            product.images = [image]
        
        # Salvar produto
        if product.save():
            result = {
                'id': product.id,
                'title': product.title,
                'handle': product.handle,
                'url': f"https://iaseoshopfy.myshopify.com/products/{product.handle}",
                'variants': [{'price': variant.price}],
                'images': [{'src': image.src}] if product.images else []
            }
            print(f"\nProduto criado com sucesso!")
            print(f"ID: {result['id']}")
            print(f"Título: {result['title']}")
            print(f"URL: {result['url']}")
            
            # Criar post no Instagram
            try:
                create_instagram_post_from_product(result)
                print("Post no Instagram criado com sucesso!")
            except Exception as instagram_error:
                print(f"Aviso: Falha ao criar post no Instagram: {str(instagram_error)}")
            
            return result
        
        raise Exception('Falha ao criar produto na Shopify')
        
    except Exception as e:
        print(f'Erro ao criar produto: {str(e)}')
        raise

if __name__ == '__main__':
    create_product()