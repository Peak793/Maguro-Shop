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
    total_price = int(request.session.get('total_price')) or 0
    duplicated = False

    for c in cart_items:
        if c.get('slug') == product.slug:
            c['qty'] = int(c.get('qty') or '1') + 1
            c['total'] = int(c.get('qty') or '1') * int(c.get('price'))
            duplicated = True

    if not duplicated:
        cart_items.append({
            'image': product.image.url,
            'id' : product.id,
            'slug' : product.slug,
            'name' : product.name,
            'price' : product.price,
            'qty': 1,
            'total': int(product.price),
        })
    request.session['cart_items'] = cart_items 
    request.session['total_price'] = total_price
    return HttpResponseRedirect(reverse('myapp:cart_list', kwargs={}))


def cart_list(request):
    cart_items = request.session.get('cart_items') or []
    total_price = int(request.session.get('total_price')) or 0
    total_qty = 0
    total_item = 0

    for c in cart_items:
        total_qty = total_qty + c.get('qty')
        total_price += int(c.get('total'))
        total_item += 1
    
    request.session['cart_qty'] = total_qty
    return render(request, 'store/cart.html', {
        'cart_items' : cart_items,
        'total_price' : total_price,
        'total_item' : total_item,
    })

def cart_delete(request,slug):
    cart_items = request.session.get("cart_items") or []
    for i in range(len(cart_items)):
        if cart_items[i]['slug'] == slug:
            del cart_items[i]
            break
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('myapp:cart_list',kwargs={}))

def inc_qty(request,slug):
    cart_items = request.session.get("cart_items") or []
    for i in range(len(cart_items)):
        if cart_items[i]['slug'] == slug:
            cart_items[i]['qty'] = int(cart_items[i]['qty']) + 1
            cart_items[i]['total'] = int(cart_items[i]['price']) * int(cart_items[i]['qty'])
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('myapp:cart_list',kwargs={}))

def dec_qty(request,slug):
    cart_items = request.session.get("cart_items") or []
    for i in range(len(cart_items)):
        if cart_items[i]['slug'] == slug:
            if int(cart_items[i]['qty']) > 1:
                cart_items[i]['qty'] = int(cart_items[i]['qty']) - 1
                cart_items[i]['total'] = int(cart_items[i]['price']) * int(cart_items[i]['qty'])
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('myapp:cart_list',kwargs={}))