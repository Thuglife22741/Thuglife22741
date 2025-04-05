from crew_automation_for_shopify_e_commerce_integration.tools.instagram_api import create_instagram_post_from_product

def main():
    # Dados do produto para postar no Instagram
    product_data = {
        'title': 'Camisa Masculina',
        'price': '29.90',
        'url': 'https://iaseoshopfy.myshopify.com/products/camisa-masculina',
        'image_url': 'https://img.kwcdn.com/product/fancy/1145de29-72c2-4fc4-ba63-5f02467b7764.jpg'
    }
    
    try:
        # Criar post no Instagram
        result = create_instagram_post_from_product(product_data)
        print('Post criado com sucesso!')
        return result
    except Exception as e:
        print(f'Erro ao criar post: {str(e)}')
        return None

if __name__ == '__main__':
    main()