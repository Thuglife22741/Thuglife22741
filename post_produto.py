from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram

# Dados do produto para teste
produto = {
    'title': 'Camiseta Estilosa',
    'price': '79.90',
    'url': 'https://example.com/camiseta-estilosa',
    'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=800&fit=crop'
}

# Tentar fazer a postagem
resultado = post_product_to_instagram(produto)
print(resultado)