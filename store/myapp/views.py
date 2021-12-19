from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, Reccom, Showcase
from django.urls.base import reverse
from .dataStructure import build_Linkedlist,sort_by_price,Queue
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
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
    '''use Structure'''
    q1_Products = Queue()
    q2_Products = Queue()
    list_of_data = []
    for x in products: #"code":x.code พวก atribute ในclass ทั้งหมด
        dict_of_data = {"code":x.code,"name":x.name,
        "slug":x.slug,
        "price":x.price,
        "description":x.description,
        "available":x.available,
        "created":x.created,
        "image":x.image,
        "category":x.category,
        }
        list_of_data.append(dict_of_data)
        q1_Products.enQueue(list_of_data)
        q2_Products.enQueue(list_of_data)
        list_of_data=[]
    q1_Products=sort_by_price(q1_Products,True)
    l1=build_Linkedlist(q1_Products)
    #print(q1_Products)
    #print(type(q1_Products))

    searched = request.session.get('searched') or ''
    if searched != '':
        temp2 = []
        if isinstance(products[0],list):
            for i in products:
                temp2.append(get_object_or_404(Product,name = i.get('name')))
            products = temp2
        temp2.clear()
        for i in products:
            if str(searched) in str(i.name).lower():
                temp2.append(i)
        products = temp2
        # products = products.filter(name__contains=searched)

    if int(s_id) == 1:
        l1.sortList(False)
        l_Products=l1.convertToArr()
        products=l_Products
        #products = products.order_by('-created')
    elif int(s_id) == 2:
        l1.sortList(True)
        l_Products=l1.convertToArr()
        products=l_Products
        #products = products.order_by('created')
    elif int(s_id) == 3:
        products = sort_by_price(q2_Products,True)
        #products = products.order_by('price')
    elif int(s_id) == 4:
        products = sort_by_price(q2_Products,False)
        #products = products.order_by('-price')

    if c:
        temp = []
        temp2 = []
        if len(products) != 0:
            if isinstance(products[0],dict):
                for i in products:
                    temp2.append(get_object_or_404(Product,name = i.get('name')))
                products = temp2
            for p in products:
                if int(p.category.id) == int(c):
                    temp.append(p)
            products = temp
        else:
            products = []
        
    categories = Category.objects.all()

    paginator = Paginator(products, 8)
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
    showcase = product.showcase.all()
    return render(request, 'store/detail.html', {
        'product': product,
        'showcase': showcase,
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
    total_price = request.session.get('total_price') or 0
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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('myapp:index')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html',{
        'form': form,
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index',kwargs={}))

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('myapp:index')
    else:
        form = UserCreationForm()
        return render(request,'account/signup.html',{
            'form':form
        })

def aboutus(request):
    return render(request,'store/aboutus.html')