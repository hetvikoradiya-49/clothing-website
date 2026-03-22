"""
Context processors for products app.
"""
from .models import Cart


def cart_item_count(request):
    """Add cart item count to all templates."""
    try:
        if request.user.is_authenticated:
            # Use filter().first() to avoid MultipleObjectsReturned
            cart = Cart.objects.filter(user=request.user).first()
            if cart is None:
                return {'cart_item_count': 0}
        else:
            session_key = request.session.session_key
            if not session_key:
                return {'cart_item_count': 0}
            # Use filter().first() to avoid MultipleObjectsReturned
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart is None:
                return {'cart_item_count': 0}
        
        item_count = sum(item.quantity for item in cart.items.all())
        return {'cart_item_count': item_count}
    except Exception:
        return {'cart_item_count': 0}
