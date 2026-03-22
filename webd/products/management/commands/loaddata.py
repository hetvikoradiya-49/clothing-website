"""
Management command to load sample data into the database.
"""
from django.core.management.base import BaseCommand
from products.models import Category, Product
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Loads sample data into the database'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Men', 'slug': 'men', 'description': 'Men\'s clothing collection'},
            {'name': 'Women', 'slug': 'women', 'description': 'Women\'s clothing collection'},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Fashion accessories'},
            {'name': 'Shoes', 'slug': 'shoes', 'description': 'Footwear collection'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample products
        products_data = [
            {
                'name': 'Classic White Shirt',
                'slug': 'classic-white-shirt',
                'description': 'A timeless white shirt crafted from premium cotton. Perfect for both formal and casual occasions.',
                'price': 89.99,
                'category': categories[0],  # Men
                'stock': 50,
                'is_available': True,
                'is_featured': True,
            },
            {
                'name': 'Slim Fit Jeans',
                'slug': 'slim-fit-jeans',
                'description': 'Modern slim fit jeans with stretch comfort. A versatile addition to any wardrobe.',
                'price': 129.99,
                'category': categories[0],  # Men
                'stock': 35,
                'is_available': True,
                'is_featured': True,
            },
            {
                'name': 'Elegant Evening Dress',
                'slug': 'elegant-evening-dress',
                'description': 'Stunning evening dress with elegant design. Perfect for special occasions.',
                'price': 199.99,
                'category': categories[1],  # Women
                'stock': 25,
                'is_available': True,
                'is_featured': True,
            },
            {
                'name': 'Summer Floral Dress',
                'slug': 'summer-floral-dress',
                'description': 'Light and breezy summer dress with beautiful floral print.',
                'price': 149.99,
                'category': categories[1],  # Women
                'stock': 40,
                'is_available': True,
                'is_featured': True,
            },
            {
                'name': 'Leather Belt',
                'slug': 'leather-belt',
                'description': 'Genuine leather belt with classic buckle. Timeless accessory for any outfit.',
                'price': 59.99,
                'category': categories[2],  # Accessories
                'stock': 100,
                'is_available': True,
                'is_featured': False,
            },
            {
                'name': 'Silk Scarf',
                'slug': 'silk-scarf',
                'description': 'Luxurious silk scarf with elegant pattern. Add sophistication to any look.',
                'price': 79.99,
                'category': categories[2],  # Accessories
                'stock': 60,
                'is_available': True,
                'is_featured': False,
            },
            {
                'name': 'Oxford Leather Shoes',
                'slug': 'oxford-leather-shoes',
                'description': 'Classic oxford shoes made from premium leather. Perfect for formal occasions.',
                'price': 249.99,
                'category': categories[3],  # Shoes
                'stock': 20,
                'is_available': True,
                'is_featured': True,
            },
            {
                'name': 'Casual Sneakers',
                'slug': 'casual-sneakers',
                'description': 'Comfortable casual sneakers with modern design. Perfect for everyday wear.',
                'price': 119.99,
                'category': categories[3],  # Shoes
                'stock': 45,
                'is_available': True,
                'is_featured': True,
            },
            {
                'name': 'Wool Blazer',
                'slug': 'wool-blazer',
                'description': 'Premium wool blazer with tailored fit. Essential for the modern gentleman.',
                'price': 299.99,
                'category': categories[0],  # Men
                'stock': 15,
                'is_available': True,
                'is_featured': False,
            },
            {
                'name': 'Cashmere Sweater',
                'slug': 'cashmere-sweater',
                'description': 'Ultra-soft cashmere sweater. Luxurious comfort for cold days.',
                'price': 179.99,
                'category': categories[1],  # Women
                'stock': 30,
                'is_available': True,
                'is_featured': False,
            },
            {
                'name': 'Leather Wallet',
                'slug': 'leather-wallet',
                'description': 'Slim leather wallet with card slots. Minimalist design meets functionality.',
                'price': 69.99,
                'category': categories[2],  # Accessories
                'stock': 80,
                'is_available': True,
                'is_featured': False,
            },
            {
                'name': 'Running Shoes',
                'slug': 'running-shoes',
                'description': 'Lightweight running shoes with responsive cushioning. Built for performance.',
                'price': 159.99,
                'category': categories[3],  # Shoes
                'stock': 55,
                'is_available': True,
                'is_featured': False,
            },
        ]
        
        for prod_data in products_data:
            category = prod_data.pop('category')
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={**prod_data, 'category': category}
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))
        self.stdout.write('Run "python manage.py runserver" to start the server.')
