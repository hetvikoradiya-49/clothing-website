"""
Models for the e-commerce products app.
"""
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Category model for organizing products."""
    DEPARTMENT_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('kids', 'Kids'),
        ('accessories', 'Accessories'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='women')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model for clothing items."""
    # Default images for each department
    DEPARTMENT_IMAGES = {
        'women': [
            'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400',
            'https://images.unsplash.com/photo-1485968579580-b6d095142e6e?w=400',
            'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=400',
            'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400',
            'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400',
        ],
        'men': [
            'https://images.unsplash.com/photo-1490578474895-699cd4e2cf59?w=400',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
            'https://images.unsplash.com/photo-1505022610485-0249ba5b3675?w=400',
            'https://images.unsplash.com/photo-1512353087810-25dfcd100962?w=400',
            'https://images.unsplash.com/photo-1475180098004-ca77a66827be?w=400',
        ],
        'kids': [
            'https://images.unsplash.com/photo-1519457431-44ccd64a579b?w=400',
            'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400',
            'https://images.unsplash.com/photo-1621452773781-0f992ee03591?w=400',
            'https://images.unsplash.com/photo-1596870230751-ebdfce98ec42?w=400',
            'https://images.unsplash.com/photo-1601342637835-59396c08f0a8?w=400',
        ],
        'accessories': [
            'https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=400',
            'https://images.unsplash.com/photo-1576053139778-7e32f2ae3cfd?w=400',
            'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400',
            'https://images.unsplash.com/photo-1560343090-f0409e92791a?w=400',
        ],
        'other': [
            'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400',
        ],
    }
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_default_image(self):
        """Get department-specific default image based on product's category."""
        department = self.category.department if self.category else 'other'
        images = self.DEPARTMENT_IMAGES.get(department, self.DEPARTMENT_IMAGES['other'])
        index = hash(self.name) % len(images)
        return images[index]
    
    def get_image_url(self):
        """Get the product image URL, or department default if no image."""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return self.get_default_image()


class Cart(models.Model):
    """Shopping cart model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    """Individual items in the cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        """Calculate total price for this cart item."""
        return self.product.price * self.quantity


class Order(models.Model):
    """Order model for completed purchases."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Debit/Credit Card'),
        ('bank', 'Bank Transfer'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"Order {self.id} - {self.user.username}"
        return f"Order {self.id} - Guest"


class OrderItem(models.Model):
    """Individual items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity


class NewsletterSubscriber(models.Model):
    """Newsletter subscription model."""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

class Review(models.Model):
    """Product review model with star rating and feedback."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, '*'*i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars for {self.product.name}"

