from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, Reccom
from django.urls.base import reverse
# Create your views here.


def index(request):
    reccom = Reccom.objects.all()
    for x in reccom:
        print(x.product.price)
    return render(request, 'index.html', {'reccom': reccom, })


def store(request):
    products = Product.objects.filter(available=True)
    c = request.GET.get('categoryid')

    if c:
        products = products.filter(category_id=int(c))

    categories = Category.objects.all()

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'store/store.html', {
        'products': products,
        'categories': categories,
        'category_id': c,
    })


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', {
        'product': product,
    })


def cart_add(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_items = request.session.get('cart_items') or []

    duplicated = False

    for c in cart_items:
        if c.get('slug') == product.slug:
            c['qty'] = int(c.get('qty') or '1') + 1
            duplicated = True

    if not duplicated:
        cart_items.append({
            'id' : product.id,
            'slug' : product.slug,
            'name' : product.name,
            'qty': 1,
        })

    return HttpResponseRedirect(reverse('myapp:cart_list', kwargs={}))


def cart_list(request):
    cart_items = request.session.get('cart_items') or []

    total_qty = 0

    for c in cart_items:
        total_qty = total_qty + c.get('qty')
    
    request.session['cart_qty'] = total_qty
    return render(request, 'store/cart.html', {
        'cart_items' : cart_items,
    })