from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram

# Dados do produto para postagem
produto = {
    'title': 'Camisa Masculina Elegante',
    'price': '159.90',
    'url': 'https://iaseoshopfy.myshopify.com/products/camisa-masculina',
    'image_url': 'https://img.kwcdn.com/product/fancy/1145de29-72c2-4fc4-ba63-5f02467b7764.jpg'
}

# Fazer a postagem no Instagram
try:
    resultado = post_product_to_instagram(produto)
    if resultado['success']:
        print('✅ Post criado com sucesso!')
        print(f"Mensagem: {resultado['message']}")
    else:
        print('❌ Erro ao criar post')
        print(f"Erro: {resultado['message']}")
        print(f"Tipo de erro: {resultado['error_type']}")
except Exception as e:
    print(f'❌ Erro inesperado: {str(e)}')