from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram
import json

def main():
    # Carregar dados do produto de teste
    try:
        with open('test_post_data.json', 'r', encoding='utf-8') as f:
            product_data = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do produto: {str(e)}")
        return
    
    # Tentar fazer a postagem no Instagram
    print("Iniciando postagem no Instagram...")
    result = post_product_to_instagram(product_data)
    
    # Verificar resultado
    if result['success']:
        print("\nSucesso!")
        print(result['message'])
    else:
        print("\nFalha!")
        print(f"Erro: {result['message']}")
        print(f"Tipo de erro: {result['error_type']}")

if __name__ == '__main__':
    main()