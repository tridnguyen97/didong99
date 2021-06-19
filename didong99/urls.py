"""didong99 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path, include
from banhang import views
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.SignUpView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.ProductView.as_view(),name='product'),
    path('<int:pk>/',views.ProductDetailView.as_view(), name='productDetail'),
    path('cart/',login_required(views.CartView.as_view()), name='cart'),
    path('orderproduct/', views.OrderView.as_view(), name='order'),
]
urlpatterns += [url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})]
