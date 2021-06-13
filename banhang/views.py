from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, edit
from django.core.paginator import Paginator
from .models import Cart, Product, Order, OrderDetail
from .forms import CartForm, UserSignUpForm, OrderForm
from django.urls import reverse_lazy
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

class ProductDetailView(edit.FormMixin,DetailView):
    context_object_name = 'product_object'
    template_name = 'product/product_detail.html'
    form_class = CartForm
    success_url = '/'

    def get_object(self):
        return Product.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        current_user = self.request.user
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)
        checkinproduct = Cart.objects.filter(product_id=product_id, user_id=current_user.id) # Check product in cart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
        if control==1: # Update  cart
            data = Cart.objects.get(product_id=product_id, user_id=current_user.id)
            data.quantity += form.cleaned_data['quantity']
            data.save()  # save data
        else : # Inser to cart
            data = Cart()
            data.user = current_user
            data.product =product
            data.quantity = form.cleaned_data['quantity']
            data.save()
        messages.success(self.request, "Product added to cart ")
        return super().form_valid(form)

class CartView(DetailView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart_object'
    
    def get_object(self):
        return Cart.objects.get(user_id=self.request.user.id, product_id = 1)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user_id=self.request.user.id)
        total=0
        for rs in cart:
            total += rs.product.price * rs.quantity
        context['cart'] = cart
        context['total'] = total
        return context

class OrderView(edit.FormView):
    template_name = 'order/order.html'
    form_class = OrderForm
    model = Order
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user_id=self.request.user.id)
        total = 0
        for rs in cart:
            total += rs.product.price * rs.quantity
        context['cart'] = cart
        context['total'] = total
        return context

    def form_valid(self, form):
        current_user = self.request.user
        cart = Cart.objects.filter(user_id=self.request.user.id)
        total = 0
        for rs in cart:
            total += rs.product.price * rs.quantity
        data = Order()
        data.first_name = form.cleaned_data['first_name'] #get product quantity from form
        data.last_name = form.cleaned_data['last_name']
        data.address = form.cleaned_data['address']
        data.city = form.cleaned_data['city']
        data.phone = form.cleaned_data['phone']
        data.user = current_user
        data.total = total
        data.save() #


        for rs in cart:
            detail = OrderDetail()
            detail.order        = Order.objects.get(pk=data.id) # Order Id
            detail.product_id   = rs.product_id
            detail.user         = current_user
            detail.quantity     = rs.quantity
            detail.price    = rs.product.price
            detail.amount        = rs.amount
            detail.save()
                
            Cart.objects.filter(user_id=current_user.id).delete() # Clear & Delete cart
            messages.success(self.request, "Your Order has been completed. Thank you ")
        return super().form_valid(form)
        
        