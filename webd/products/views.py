"""
Views for the e-commerce products app.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Category, Product, Cart, CartItem, Order, OrderItem, NewsletterSubscriber, Review
from django.db.models import Avg


def home(request):
    """Home page view with featured products."""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    categories = Category.objects.all()[:10]
    latest_products = Product.objects.filter(is_available=True)[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'products/home.html', context)


def new_arrival(request):
    """New Arrival page - shows latest products."""
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:20]
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'page_title': 'New Arrivals',
    }
    return render(request, 'products/new_arrival.html', context)


def most_likely(request):
    """Most Likely page - shows featured/popular products."""
    products = Product.objects.filter(is_featured=True, is_available=True).order_by('-created_at')[:20]
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'page_title': 'Most Popular',
    }
    return render(request, 'products/most_likely.html', context)


def shop(request):
    """Shop page with all products and filtering."""
    category_id = request.GET.get('category')
    products = Product.objects.filter(is_available=True)
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'products/shop.html', context)


def product_detail(request, slug):
    """Product detail page with reviews and feedback."""

    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if rating and 1 <= int(rating) <= 5:
            # Check if user already reviewed
            user_review = product.reviews.filter(user=request.user).first()
            if not user_review:
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=int(rating),
                    comment=comment
                )
                messages.success(request, 'Review added successfully!')
            else:
                messages.info(request, 'You have already reviewed this product.')
        else:
            messages.error(request, 'Please select a valid rating (1-5 stars).')
    
    # Fetch reviews and stats
    reviews = product.reviews.all().order_by('-created_at')[:10]
    avg_rating = product.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Check if user can review
    can_review = (
        request.user.is_authenticated and 
        not product.reviews.filter(user=request.user).exists()
    )
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'can_review': can_review,
    }
    return render(request, 'products/product_detail.html', context)


def about(request):
    """About page."""
    return render(request, 'products/about.html')


def contact(request):
    """Contact page."""
    return render(request, 'products/contact.html')


def cart(request):
    """Shopping cart page."""
    cart_obj = get_or_create_cart(request)
    items = cart_obj.items.all()
    
    total = sum(item.total_price for item in items)
    
    context = {
        'cart': cart_obj,
        'items': items,
        'total': total,
    }
    return render(request, 'products/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart_obj = get_or_create_cart(request)
    
    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart_obj,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Get cart count for response
    cart_count = sum(item.quantity for item in cart_obj.items.all())
    
    # Return JSON response for AJAX
    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart!',
        'cart_count': cart_count
    })


@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')


@require_POST
def remove_cart_item(request, item_id):
    """Remove item from cart."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


def checkout(request):
    """Checkout page."""
    # Check if user is logged in, if not redirect to login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to proceed with checkout.')
        return redirect(f'login?next={request.path}')
    
    cart_obj = get_or_create_cart(request)
    items = cart_obj.items.all()
    
    if not items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('shop')
    
    total = sum(item.total_price for item in items)
    
    if request.method == 'POST':
        # Store checkout info in session for payment page
        request.session['checkout_first_name'] = request.POST.get('first_name')
        request.session['checkout_last_name'] = request.POST.get('last_name')
        request.session['checkout_email'] = request.POST.get('email')
        request.session['checkout_phone'] = request.POST.get('phone')
        request.session['checkout_address'] = request.POST.get('address')
        request.session['checkout_city'] = request.POST.get('city')
        request.session['checkout_postal_code'] = request.POST.get('postal_code')
        request.session['checkout_country'] = request.POST.get('country')
        request.session['checkout_notes'] = request.POST.get('notes', '')
        
        return redirect('payment')
    
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'products/checkout.html', context)


def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'products/order_confirmation.html', context)


def register(request):
    """User registration page."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'products/register.html', context)


def login_view(request):
    """User login page."""
    next_url = request.GET.get('next', 'home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Merge guest cart with user cart
                session_key = request.session.session_key
                if session_key:
                    guest_cart = Cart.objects.filter(session_key=session_key).first()
                    if guest_cart and guest_cart.items.exists():
                        user_cart, _ = Cart.objects.get_or_create(user=user)
                        for item in guest_cart.items.all():
                            existing_item = user_cart.items.filter(product=item.product).first()
                            if existing_item:
                                existing_item.quantity += item.quantity
                                existing_item.save()
                            else:
                                item.cart = user_cart
                                item.save()
                        guest_cart.delete()
                
                messages.success(request, f'Welcome back, {username}!')
                if next_url and next_url != 'home':
                    return redirect(next_url)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'products/login.html', context)


def logout_view(request):
    """User logout."""
    logout(request)
    messages.info(request, 'You have been logged out!')
    return redirect('home')


@require_POST
def subscribe_newsletter(request):
    """Subscribe to newsletter."""
    email = request.POST.get('email')
    
    if email:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            messages.success(request, 'Thank you for subscribing!')
        else:
            messages.info(request, 'You are already subscribed!')
    
    return redirect('home')


def get_or_create_cart(request):
    """Get or create cart for user/session - always returns single cart."""
    try:
        if request.user.is_authenticated:
            # Use filter().first() to avoid MultipleObjectsReturned
            cart = Cart.objects.filter(user=request.user).first()
            if cart is None:
                cart = Cart.objects.create(user=request.user)
            # Clean up any duplicate carts for this user
            Cart.objects.filter(user=request.user).exclude(id=cart.id).delete()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            # Use filter().first() to avoid MultipleObjectsReturned
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart is None:
                cart = Cart.objects.create(session_key=session_key)
            # Clean up any duplicate carts for this session
            Cart.objects.filter(session_key=session_key).exclude(id=cart.id).delete()
        return cart
    except Exception:
        # Fallback: try to get any cart or create new one
        if request.user.is_authenticated:
            return Cart.objects.filter(user=request.user).first() or Cart.objects.create(user=request.user)
        else:
            session_key = request.session.session_key or 'temp_session'
            return Cart.objects.filter(session_key=session_key).first() or Cart.objects.create(session_key=session_key)


def cart_item_count(request):
    """Context processor for cart item count."""
    try:
        cart_obj = get_or_create_cart(request)
        if cart_obj is None:
            return {'cart_item_count': 0}
        item_count = sum(item.quantity for item in cart_obj.items.all())
        return {'cart_item_count': item_count}
    except Exception:
        return {'cart_item_count': 0}


def payment(request):
    """Payment page view."""
    try:
        # Use get_or_create_cart helper function for consistent cart handling
        cart_obj = get_or_create_cart(request)
        items = cart_obj.items.all()
        
        if not items:
            messages.warning(request, 'Your cart is empty!')
            return redirect('shop')
        
        total = sum(item.total_price for item in items)
        
        # Get checkout info from session
        first_name = request.session.get('checkout_first_name', '')
        last_name = request.session.get('checkout_last_name', '')
        email = request.session.get('checkout_email', '')
        phone = request.session.get('checkout_phone', '')
        address = request.session.get('checkout_address', '')
        city = request.session.get('checkout_city', '')
        postal_code = request.session.get('checkout_postal_code', '')
        country = request.session.get('checkout_country', '')
        notes = request.session.get('checkout_notes', '')
        
        if request.method == 'POST':
            payment_method = request.POST.get('payment_method', 'cash')
            
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                country=country,
                total_amount=total,
                payment_method=payment_method,
                payment_status='completed',
                status='processing',
                notes=notes,
            )
            
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear cart and session
            cart_obj.items.all().delete()
            for key in ['checkout_first_name', 'checkout_last_name', 'checkout_email', 
                        'checkout_phone', 'checkout_address', 'checkout_city', 
                        'checkout_postal_code', 'checkout_country', 'checkout_notes']:
                if key in request.session:
                    del request.session[key]
            
            # Get payment method display name
            payment_method_names = {
                'cash': 'Cash on Delivery',
                'upi': 'UPI',
                'card': 'Debit/Credit Card',
                'bank': 'Bank Transfer',
            }
            payment_method_name = payment_method_names.get(payment_method, 'Cash on Delivery')
            
            return render(request, 'products/payment.html', {
                'success': True,
                'order_id': order.id,
                'total': total,
                'payment_method': payment_method,
                'payment_method_name': payment_method_name,
            })
        
        context = {
            'items': items,
            'total': total,
        }
        return render(request, 'products/payment.html', context)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('cart')
