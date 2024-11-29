from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Kategori, Cart, CartItem, Order, OrderItem

def product_list(request):
    categories = Kategori.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'categories': categories, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    item = cart.item.all()
    total = sum(item.products.price * item.quantity for item in item)
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'item': item, 'total' : total})

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    order = Order.objects.create(
        user=request.user,
        total_amount= total)
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.products,
            price = item.products.price
        )
    cart.items.all().delete()  # Clear the cart after checkout
    return render(request, 'shop/order_confirmation.html', {'order': order})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

    product.review_set.create(user=request.user, rating=rating, comment=comment)
    return redirect('product_detail', slug=product.slug)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Ambil produk berdasarkan ID
    if request.method == 'POST':
        rating = request.POST.get('rating')  # Ambil rating dari form
        comment = request.POST.get('comment')  # Ambil komentar dari form
        # Buat ulasan baru (sesuaikan dengan model ulasan jika ada)
        product.review_set.create(user=request.user, rating=rating, comment=comment)
    return redirect('product_detail', slug=product.slug)
# Create your views here.
