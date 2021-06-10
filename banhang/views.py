from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, edit
from django.core.paginator import Paginator
from .models import Product
from .forms import UserSignUpForm
from django.urls import reverse_lazy

# Create your views here.

class SignUpView(edit.CreateView):
    template_name = "signup.html"
    success_url = reverse_lazy('login')
    form_class = UserSignUpForm
    success_message = "Your profile was created successfully"

class ProductView(View):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def get(self, *arg, **kwargs):
        product_objects = Product.objects.all()

        # paginator code
        paginator = Paginator(product_objects, 4)
        page = self.request.GET.get('page')
        product_objects = paginator.get_page(page)
        return render(self.request,'index.html',{'product_objects':product_objects})

class ProductDetailView(DetailView):
    context_object_name = 'product_object'
    template_name = 'product_detail.html'
    
    def get_object(self):
        return Product.objects.get(pk=self.kwargs['uuid'])

    