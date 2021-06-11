from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, edit
from django.core.paginator import Paginator
from .models import Cart, Product
from .forms import CartForm, UserSignUpForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

class SignUpView(edit.CreateView):
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')
    form_class = UserSignUpForm
    success_message = "Your profile was created successfully"

class ProductView(View):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def get(self, *arg, **kwargs):
        product_objects = Product.objects.all()
        # paginator 
        paginator = Paginator(product_objects, 4)
        page = self.request.GET.get('page')
        product_objects = paginator.get_page(page)
        return render(self.request,'index.html',{'product_objects':product_objects})

class ProductDetailView(DetailView):
    context_object_name = 'product_object'
    template_name = 'product_detail.html'

    def get_object(self):
        return Product.objects.get(pk=self.kwargs['pk'])

class AddCartView(edit.FormView):
    form_class = CartForm
    template_name = 'cart.html'
    success_url = '/'

    def form_valid(self, form):
        current_user = self.request.user
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)
        checkinproduct = Cart.objects.filter(product_id=product_id, user_id=current_user.id) # Check product in shopcart
        data = self.get_context_data()
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
        if control==1: # Update  shopcart
            data = Cart.objects.get(product_id=product_id, user_id=current_user.id)
            data.quantity += form.cleaned_data['quantity']
            data.save()  # save data
            print('Cart has been added')
        else : # Inser to Shopcart
            data = Cart()
            data.user = current_user
            data.product =product
            data.quantity = form.cleaned_data['quantity']
            data.save()
        messages.success(self.request, "Product added to Shopcart ")
        return super().form_valid(form)
    
