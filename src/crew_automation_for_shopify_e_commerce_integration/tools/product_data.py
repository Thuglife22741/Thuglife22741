"""Module for managing product data and creating sales pages."""

def get_product_data():
    """Get the product data for the sales page."""
    return {
        'title': 'Caderno Personalizado Exclusivo',
        'description': '''
        <div class="product-description">
            <h2>Caderno Personalizado Único e Especial</h2>
            <p>Transforme suas anotações em algo extraordinário com nosso Caderno Personalizado Premium!</p>
            
            <h3>Características Principais:</h3>
            <ul>
                <li>✨ Design totalmente personalizável</li>
                <li>📝 200 páginas de papel de alta qualidade</li>
                <li>🎨 Capa durável e elegante</li>
                <li>📏 Tamanho A5 perfeito para carregar</li>
                <li>🎁 Embalagem premium para presente</li>
            </ul>
            
            <h3>Por que Escolher Nosso Caderno?</h3>
            <p>Cada caderno é único como você! Personalize com seu nome, frases inspiradoras ou designs exclusivos.</p>
            
            <h3>Especificações:</h3>
            <ul>
                <li>Material: Capa dura premium</li>
                <li>Páginas: 200 (papel 90g)</li>
                <li>Dimensões: 14.8 x 21 cm (A5)</li>
                <li>Acabamento: Costura reforçada</li>
            </ul>
            
            <h3>Garantia de Satisfação</h3>
            <p>Oferecemos garantia de 30 dias e frete grátis para todo o Brasil!</p>
        </div>
        ''',
        'price': '89.90',
        'compare_at_price': '129.90',
        'images': [
            'https://cdn.shopify.com/s/files/1/0704/0158/7460/files/caderno-personalizado-1.jpg',
            'https://cdn.shopify.com/s/files/1/0704/0158/7460/files/caderno-personalizado-2.jpg',
            'https://cdn.shopify.com/s/files/1/0704/0158/7460/files/caderno-personalizado-3.jpg'
        ],
        'variants': [
            {
                'title': 'Clássico',
                'price': '89.90',
                'inventory_quantity': 50
            },
            {
                'title': 'Premium',
                'price': '119.90',
                'inventory_quantity': 30
            },
            {
                'title': 'Luxo',
                'price': '149.90',
                'inventory_quantity': 20
            }
        ]
    }