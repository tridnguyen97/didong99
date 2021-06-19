def carts(request):
    from banhang.models import Cart
    return {'carts': Cart.objects.filter(user_id=request.user.id)}