from django.shortcuts import render, get_object_or_404, redirect
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'product_detail.html', {
        'product': product
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):

    cart_data = request.session.get('cart', {})

    cart_products = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity

        total += item_total

        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'cart.html', {
        'cart_products': cart_products,
        'total': total
    })


def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')