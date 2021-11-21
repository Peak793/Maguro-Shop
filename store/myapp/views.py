from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Category, Product,Reccom
# Create your views here.
def index(request):
    reccom = Reccom.objects.all()
    return render(request, 'index.html',{'reccom':reccom,})

def store(request):
    products = Product.objects.filter(available = True)
    categories = Category.objects.all()
                                                                
    paginator = Paginator(products,12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,'store/store.html',{'products':products,'categories':categories})

def detail(request,slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'store/detail.html',{
        'product':product,
    })