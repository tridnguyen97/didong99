from banhang.models import Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField

class UserSignUpForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ['username','email', 'first_name']

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','phone','city','country']