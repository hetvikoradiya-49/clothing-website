"""
Admin configuration for products app.
"""
from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, NewsletterSubscriber


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'department', 'created_at']
    list_filter = ['department']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'category', 'stock', 'is_available', 'is_featured', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available', 'is_featured']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__username', 'first_name', 'last_name', 'email']
    list_editable = ['status']
    inlines = [OrderItemInline]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
