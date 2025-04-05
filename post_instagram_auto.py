from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram

# Dados do produto para teste
produto = {
    'title': 'Tênis Esportivo Premium',
    'price': '299.90',
    'url': 'https://example.com/tenis-esportivo',
    'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop'
}

# Tentar fazer a postagem
resultado = post_product_to_instagram(produto)
print(resultado)