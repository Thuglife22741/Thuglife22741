from src.crew_automation_for_shopify_e_commerce_integration.tools.post_automation import post_product_to_instagram
import json

with open('test_product.json', 'r', encoding='utf-8') as f:
    product_data = json.load(f)

result = post_product_to_instagram(product_data)
print(json.dumps(result, indent=2))