/**
 * LUXE Fashion - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initMessageClose();
    initQuantityButtons();
    initSmoothScroll();
    initCustomerServicePopup();
    initAddToCart();
});

/**
 * Add to Cart AJAX Handler
 */
function initAddToCart() {
    // Handle all add to cart forms
    document.querySelectorAll('form[action*="add-to-cart"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.action;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count in navbar
                    const cartCountElement = document.querySelector('.cart-count');
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count;
                        cartCountElement.style.display = 'block';
                    } else {
                        // Create cart count badge if doesn't exist
                        const cartBtn = document.querySelector('.cart-btn');
                        if (cartBtn) {
                            const countSpan = document.createElement('span');
                            countSpan.className = 'cart-count';
                            countSpan.textContent = data.cart_count;
                            cartBtn.appendChild(countSpan);
                        }
                    }
                    
                    // Show success popup
                    showAddToCartPopup(data.message);
                }
            })
            .catch(error => {
                console.error('Error adding to cart:', error);
                showAddToCartPopup('Error adding to cart. Please try again.');
            });
        });
    });
}

/**
 * Show Add to Cart Popup
 */
function showAddToCartPopup(message) {
    // Remove existing popup if any
    const existingPopup = document.querySelector('.add-to-cart-popup');
    if (existingPopup) {
        existingPopup.remove();
    }
    
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'add-to-cart-popup';
    popup.innerHTML = `
        <div class="popup-content">
            <div class="popup-icon">✓</div>
            <p>${message}</p>
            <div class="popup-buttons">
                <a href="/cart/" class="btn-view-cart">View Cart</a>
                <button class="btn-continue-shopping">Continue Shopping</button>
            </div>
        </div>
    `;
    
    // Add styles
    popup.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        z-index: 10000;
        text-align: center;
        animation: popupFadeIn 0.3s ease;
        min-width: 300px;
    `;
    
    // Add popup icon styles
    const icon = popup.querySelector('.popup-icon');
    icon.style.cssText = `
        width: 60px;
        height: 60px;
        background: #28a745;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin: 0 auto 1rem;
    `;
    
    // Add button styles
    const buttons = popup.querySelector('.popup-buttons');
    buttons.style.cssText = `
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1.5rem;
    `;
    
    const viewCartBtn = popup.querySelector('.btn-view-cart');
    viewCartBtn.style.cssText = `
        padding: 0.75rem 1.5rem;
        background: #333;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        transition: background 0.3s;
    `;
    
    const continueBtn = popup.querySelector('.btn-continue-shopping');
    continueBtn.style.cssText = `
        padding: 0.75rem 1.5rem;
        background: transparent;
        border: 2px solid #333;
        color: #333;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    `;
    
    // Add continue shopping click handler
    continueBtn.addEventListener('click', function() {
        popup.remove();
        document.body.style.overflow = '';
    });
    
    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes popupFadeIn {
            from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
            to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        }
    `;
    document.head.appendChild(style);
    
    // Add overlay
    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay-addtocart';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 9999;
    `;
    
    overlay.addEventListener('click', function() {
        popup.remove();
        overlay.remove();
        document.body.style.overflow = '';
    });
    
    document.body.appendChild(overlay);
    document.body.appendChild(popup);
    document.body.style.overflow = 'hidden';
    
    // Auto close after 5 seconds
    setTimeout(() => {
        if (popup.parentNode) {
            popup.remove();
            overlay.remove();
            document.body.style.overflow = '';
        }
    }, 5000);
}

/**
 * Customer Service Popup
 */
function initCustomerServicePopup() {
    const popup = document.getElementById('customerServicePopup');
    const popupContent = document.getElementById('popupContent');
    const closeBtn = document.getElementById('popupClose');
    const serviceLinks = document.querySelectorAll('.customer-service-link');
    
    // Service content data
    const serviceData = {
        shipping: {
            icon: '<i class="fas fa-shipping-fast service-icon"></i>',
            title: 'Shipping Information',
            content: `
                <p>We offer free standard shipping on all orders above ₹500. Express delivery options are also available.</p>
                <ul>
                    <li><strong>Standard Shipping:</strong> 5-7 business days - Free</li>
                    <li><strong>Express Shipping:</strong> 2-3 business days - ₹199</li>
                    <li><strong>Next Day Delivery:</strong> Order before 2pm - ₹399</li>
                </ul>
                <p>International shipping available to select countries. Customs charges may apply.</p>
            `
        },
        returns: {
            icon: '<i class="fas fa-undo-alt service-icon"></i>',
            title: 'Returns & Exchanges',
            content: `
                <p>We want you to love your purchase. If you're not completely satisfied, we offer easy returns.</p>
                <ul>
                    <li>30-day return policy for all items</li>
                    <li>Items must be unworn with original tags attached</li>
                    <li>Free return shipping for exchanges</li>
                    <li>Refund processed within 5-7 business days</li>
                </ul>
                <p>To initiate a return, please contact our customer service team.</p>
            `
        },
        'order-status': {
            icon: '<i class="fas fa-clipboard-check service-icon"></i>',
            title: 'Order Status',
            content: `
                <p>Track your order status easily through our tracking system.</p>
                <ul>
                    <li><strong>Order Confirmed:</strong> We've received your order</li>
                    <li><strong>Processing:</strong> Your order is being prepared</li>
                    <li><strong>Shipped:</strong> On its way to you</li>
                    <li><strong>Delivered:</strong> Package has arrived</li>
                </ul>
                <p>You'll receive tracking details via email once your order ships.</p>
            `
        },
        faq: {
            icon: '<i class="fas fa-question-circle service-icon"></i>',
            title: 'Frequently Asked Questions',
            content: `
                <p><strong>Q: How do I find my size?</strong></p>
                <p>A: Please refer to our size chart on each product page.</p>
                
                <p><strong>Q: Can I change my order after placing it?</strong></p>
                <p>A: Contact us within 1 hour of placing your order.</p>
                
                <p><strong>Q: Do you ship internationally?</strong></p>
                <p>A: Yes, we ship to over 50 countries worldwide.</p>
                
                <p><strong>Q: How can I contact customer service?</strong></p>
                <p>A: Reach us at support@luxefashion.com or call +91 98765 43210</p>
            `
        }
    };
    
    // Open popup when clicking on service links
    serviceLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const service = this.getAttribute('data-service');
            
            if (serviceData[service]) {
                popupContent.innerHTML = serviceData[service].icon + 
                    '<h3>' + serviceData[service].title + '</h3>' + 
                    serviceData[service].content;
                popup.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    // Close popup when clicking close button
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            popup.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Close popup when clicking overlay
    if (popup) {
        popup.addEventListener('click', function(e) {
            if (e.target === popup) {
                popup.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Close popup with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && popup.classList.contains('active')) {
            popup.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const menuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    
    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Animate hamburger
            const spans = menuBtn.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!menuBtn.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                const spans = menuBtn.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
}

/**
 * Close Messages
 */
function initMessageClose() {
    const closeButtons = document.querySelectorAll('.message-close');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}

/**
 * Quantity Buttons
 */
function initQuantityButtons() {
    // Add slideOut animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

/**
 * Smooth Scroll
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Product Slider (for future use)
 */
class ProductSlider {
    constructor(element) {
        this.element = element;
        this.container = element.querySelector('.slider-container');
        this.slides = this.container ? this.container.querySelectorAll('.slide') : [];
        this.currentIndex = 0;
        this.prevBtn = element.querySelector('.slider-btn.prev');
        this.nextBtn = element.querySelector('.slider-btn.next');
        
        this.init();
    }
    
    init() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
    }
    
    update() {
        if (this.container && this.slides.length > 0) {
            const slideWidth = this.slides[0].offsetWidth;
            this.container.style.transform = `translateX(-${this.currentIndex * slideWidth}px)`;
        }
    }
    
    next() {
        if (this.currentIndex < this.slides.length - 1) {
            this.currentIndex++;
            this.update();
        }
    }
    
    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.update();
        }
    }
}

// Initialize sliders
document.querySelectorAll('.product-slider').forEach(slider => {
    new ProductSlider(slider);
});

/**
 * Cart Quantity Update (AJAX - optional enhancement)
 */
function updateCartItem(itemId, quantity) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/update-cart/${itemId}/`;
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'csrfmiddlewaretoken';
        input.value = csrfToken.value;
        form.appendChild(input);
    }
    
    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity;
    form.appendChild(quantityInput);
    
    document.body.appendChild(form);
    form.submit();
}

/**
 * Newsletter Form Validation
 */
function validateNewsletterForm(form) {
    const email = form.querySelector('input[type="email"]');
    
    if (email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!emailRegex.test(email.value)) {
            alert('Please enter a valid email address.');
            return false;
        }
    }
    
    return true;
}

// Add newsletter validation
document.querySelectorAll('.newsletter-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!validateNewsletterForm(this)) {
            e.preventDefault();
        }
    });
});

/**
 * Form Validation Utilities
 */
const FormValidator = {
    email: function(value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value);
    },
    
    phone: function(value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        return value.length >= 10 && phoneRegex.test(value);
    },
    
    required: function(value) {
        return value.trim().length > 0;
    },
    
    minLength: function(value, min) {
        return value.trim().length >= min;
    }
};

// Export for use in other scripts
window.LUXE = {
    ProductSlider,
    FormValidator,
    updateCartItem
};
app.get("/", (req, res) => {
  res.send("API is running");
});
