"""Exemplo de como fazer uma publicação no Instagram."""

from ..tools.post_automation import post_product_to_instagram

def main():
    # Exemplo de dados do produto
    produto_exemplo = {
        'title': 'Camiseta Estilosa',
        'price': '89.90',
        'url': 'https://minha-loja.myshopify.com/products/camiseta-estilosa',
        'image_url': 'https://cdn.shopify.com/s/files/1/0xxx/0xxx/products/camiseta.jpg'
    }
    
    # Fazer a postagem no Instagram
    resultado = post_product_to_instagram(produto_exemplo)
    
    if resultado['success']:
        print('✅ Post criado com sucesso!')
        print(f"Mensagem: {resultado['message']}")
    else:
        print('❌ Erro ao criar post')
        print(f"Erro: {resultado['message']}")
        print(f"Tipo de erro: {resultado['error_type']}")

if __name__ == '__main__':
    main()