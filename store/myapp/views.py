from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, Reccom
from django.urls.base import reverse
# Create your views here.

def index(request):
    request.session['sort_id'] = None
    request.session['sort_name'] = 'จัดเรียงตาม'
    request.session['searched'] = ''
    reccom = Reccom.objects.all()
    return render(request, 'index.html', {'reccom': reccom, })


def store(request):
    products = Product.objects.filter(available=True)
    s_name = request.session.get('sort_name') or 'จัดเรียงตาม'
    s_id = request.session.get('sort_id') or 0
    c = request.session.get('category') or 0 
    
    searched = request.session.get('searched') or ''
    if searched != '':
        products = products.filter(name__contains=searched)

    if int(s_id) == 1:
        products = products.order_by('-created')
    elif int(s_id) == 2:
        products = products.order_by('created')
    elif int(s_id) == 3:
        products = products.order_by('price')
    elif int(s_id) == 4:
        products = products.order_by('-price')

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
        'sortid' : s_id,
        'sortname' : s_name,
    })

def detail(request, slug):
    request.session['sort_id'] = None
    request.session['sort_name'] = 'จัดเรียงตาม'
    request.session['searched'] = ''
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', {
        'product': product,
    })


def cart_add(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_items = request.session.get('cart_items') or []
    total_price = request.session.get('total_price') or 0
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

def category(request, categoryid):
    if int(categoryid) == 0:
        request.session['category'] = None
    else:
        request.session['category'] = categoryid
    return HttpResponseRedirect(reverse('myapp:store',kwargs={}))

def sort(request, sortid):
    if int(sortid) == 0:
        request.session['sort_id'] = None
        request.session['sort_name'] = 'จัดเรียงตาม'
    else:
        request.session['sort_id'] = sortid
        if int(sortid) == 1:
            request.session['sort_name'] = 'วันที่:ใหม่-เก่า'
        elif int(sortid) == 2:
            request.session['sort_name'] = 'วันที่:เก่า-ใหม่'
        elif int(sortid) == 3:
            request.session['sort_name'] = 'ราคา:น้อย - มาก'
        elif int(sortid) == 4:
            request.session['sort_name'] = 'ราคา:มาก - น้อย'
    return HttpResponseRedirect(reverse('myapp:store',kwargs={}))

def search_item(request):
    if request.method == 'POST':
        request.session['searched'] = request.POST['searched']
    return HttpResponseRedirect(reverse('myapp:store',kwargs={}))
