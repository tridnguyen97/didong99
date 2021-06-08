from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import Product, User
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    product_objects = Product.objects.all()

    # paginator code
    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    return render(request,'index.html',{'product_objects':product_objects})

def signup(request):
    signupForm = UserCreationForm

def detail(request,uuid):
    product_object = Product.objects.get(uuid=uuid)
    return render(request,'product_detail.html',{'product_object': product_object})
