from banhang.models import Cart
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