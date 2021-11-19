from typing import Concatenate
from django.shortcuts import render
from .models import Category, Product,Reccom
# Create your views here.
def index(request):
    reccom = Reccom.objects.all()
    return render(request, 'index.html',{'reccom':reccom,})

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request,'store.html',{'products':products,'categories':categories})