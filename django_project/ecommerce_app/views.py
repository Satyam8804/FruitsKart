from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from .models import Product, Order, LineItem
from .forms import CartForm, CheckoutForm
from . import cart

# Create your views here.


def index(request):
    all_products = Product.objects.all()
    return render(request, "ecommerce_app/index.html", {
                                    'all_products': all_products,
                                    })


def show_product(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'product_id': product.id})
    return render(request, 'ecommerce_app/product_detail.html', {
                                            'product': product,
                                            'form': form,
                                            })


def show_cart(request):

    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'ecommerce_app/cart.html', {
                                            'cart_items': cart_items,
                                            'cart_subtotal': cart_subtotal,
                                            })
from .forms import CheckoutForm
from .models import CartItem, Order, LineItem
from django.contrib import messages
from django.shortcuts import render, redirect

def checkout(request):
    session_cart_id = request.session.get('cart_id')
    
    # Check if session_cart_id is not None before filtering cart items
    if session_cart_id is not None:
        cart_items = CartItem.objects.filter(cart_id=session_cart_id)

        subtotal = sum(item.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        subtotal = 0

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o = Order(
                name=cleaned_data.get('name'),
                email=cleaned_data.get('email'),
                postal_code=cleaned_data.get('postal_code'),
                address=cleaned_data.get('address'),
            )
            o.save()

            for cart_item in cart_items:
                li = LineItem(
                    product_id=cart_item.product_id,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    order=o
                )
                li.save()

            request.session['cart_id'] = 1234

            messages.add_message(request, messages.INFO, 'Order Placed!')
            return redirect('checkout')
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
    }

    return render(request, 'ecommerce_app/checkout.html', context)
