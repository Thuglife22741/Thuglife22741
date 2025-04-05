from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram

# Dados do produto para teste
produto = {
    'title': 'Produto Teste',
    'price': '99.99',
    'url': 'https://example.com/produto',
    'image_url': 'https://picsum.photos/800/800'
}

# Tentar fazer a postagem
resultado = post_product_to_instagram(produto)
print(resultado)