"""
Management command to update existing accessories products with images from image/aecessories folder.
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product


class Command(BaseCommand):
    help = 'Update existing accessories products with images from image/aecessories folder'

    def handle(self, *args, **options):
        # Source and destination paths
        source_folder = os.path.join(settings.BASE_DIR, 'image', 'aecessories')
        dest_folder = os.path.join(settings.MEDIA_ROOT, 'products')
        
        # Create destination folder if it doesn't exist
        os.makedirs(dest_folder, exist_ok=True)
        
        # Map existing products to images
        products_to_update = [
            {
                'product_slug': 'leather-belt',
                'filename': 'leather belt.jpg',
            },
            {
                'product_slug': 'leather-wallet',
                'filename': 'leatherwallet.jpg',
            },
            {
                'product_slug': 'silk-scarf',
                'filename': 'silk scarf.jpg',
            },
        ]
        
        for item in products_to_update:
            product = Product.objects.filter(slug=item['product_slug']).first()
            
            if not product:
                self.stdout.write(self.style.WARNING(f'Product not found: {item["product_slug"]}'))
                continue
            
            filename = item['filename']
            source_path = os.path.join(source_folder, filename)
            
            # Check if source file exists
            if not os.path.exists(source_path):
                self.stdout.write(self.style.WARNING(f'Image not found: {source_path}'))
                continue
            
            # Destination path
            dest_filename = f"accessories_{filename}"
            dest_path = os.path.join(dest_folder, dest_filename)
            
            # Copy file if it doesn't exist in destination
            if not os.path.exists(dest_path):
                shutil.copy2(source_path, dest_path)
                self.stdout.write(f'Copied: {filename} -> media/products/{dest_filename}')
            else:
                self.stdout.write(f'File already exists: {dest_filename}')
            
            # Update product with new image
            product.image = f'products/{dest_filename}'
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Updated product: {product.name} with image {dest_filename}'))
        
        self.stdout.write(self.style.SUCCESS('\nAccessories products updated with images successfully!'))

