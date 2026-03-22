"""
Management command to add shoes from image/shoes folder to the database.
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Add shoes from image/shoes folder to the database'

    def handle(self, *args, **options):
        # Source and destination paths
        source_folder = os.path.join(settings.BASE_DIR, 'image', 'shoes')
        dest_folder = os.path.join(settings.MEDIA_ROOT, 'products')
        
        # Create destination folder if it doesn't exist
        os.makedirs(dest_folder, exist_ok=True)
        
        # Get or create Shoes category
        shoes_category, created = Category.objects.get_or_create(
            slug='shoes',
            defaults={
                'name': 'Shoes',
                'description': 'Footwear collection',
                'department': 'other'
            }
        )
        if created:
            self.stdout.write(f'Created category: {shoes_category.name}')
        else:
            self.stdout.write(f'Using existing category: {shoes_category.name}')
        
        # Define shoe products data
        shoes_data = [
            {
                'filename': 'download (2).jpg',
                'name': 'Classic Leather Shoe',
                'slug': 'classic-leather-shoe',
                'description': 'Premium leather shoes with elegant design. Perfect for formal occasions and professional wear.',
                'price': 249.99,
                'stock': 25,
                'is_featured': True,
            },
            {
                'filename': 'download (4) - Copy.jpg',
                'name': 'Casual Walking Shoe',
                'slug': 'casual-walking-shoe',
                'description': 'Comfortable casual shoes with modern design. Ideal for everyday wear and light activities.',
                'price': 159.99,
                'stock': 40,
                'is_featured': True,
            },
            {
                'filename': 'red nike dunk.jpg',
                'name': 'Red Nike Dunk',
                'slug': 'red-nike-dunk',
                'description': 'Stylish Red Nike Dunk sneakers. Bold colorway with premium comfort and durability.',
                'price': 199.99,
                'stock': 30,
                'is_featured': True,
            },
        ]
        
        # Process each shoe
        for shoe in shoes_data:
            filename = shoe['filename']
            source_path = os.path.join(source_folder, filename)
            
            # Check if source file exists
            if not os.path.exists(source_path):
                self.stdout.write(self.style.WARNING(f'Image not found: {source_path}'))
                continue
            
            # Destination path
            dest_filename = filename
            dest_path = os.path.join(dest_folder, dest_filename)
            
            # Copy file if it doesn't exist in destination
            if not os.path.exists(dest_path):
                shutil.copy2(source_path, dest_path)
                self.stdout.write(f'Copied: {filename} -> media/products/')
            else:
                self.stdout.write(f'File already exists: {dest_filename}')
            
            # Create or update product in database
            product_data = {
                'name': shoe['name'],
                'slug': shoe['slug'],
                'description': shoe['description'],
                'price': shoe['price'],
                'category': shoes_category,
                'stock': shoe['stock'],
                'is_available': True,
                'is_featured': shoe['is_featured'],
            }
            
            # For the image field, we need to use the relative path
            product, created = Product.objects.get_or_create(
                slug=shoe['slug'],
                defaults={
                    **product_data,
                    'image': f'products/{dest_filename}'
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                # Update existing product
                for key, value in product_data.items():
                    setattr(product, key, value)
                product.image = f'products/{dest_filename}'
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Updated product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('\nShoes added successfully!'))
        self.stdout.write('Run "python manage.py runserver" to see the products on the website.')

