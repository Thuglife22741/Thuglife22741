from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram

# Dados do produto para teste
produto = {
    'title': 'Camisa Casual Elegante',
    'price': '159.90',
    'url': 'https://example.com/camisa-casual',
    'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&h=800&fit=crop'
}

# Tentar fazer a postagem
resultado = post_product_to_instagram(produto)
print(resultado)