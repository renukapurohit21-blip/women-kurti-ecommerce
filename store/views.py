from django.shortcuts import render, get_object_or_404, redirect
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {
        'product': product
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('home')


def buy_now(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_items = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart_items.items():
        product = Product.objects.filter(id=product_id).first()

        if product:
            subtotal = product.price * quantity

            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

            total += subtotal

    return render(request, 'store/cart.html', {
        'cart_items': products,
        'total': total,
    })


def contact(request):
    return render(request, 'store/contact.html')
