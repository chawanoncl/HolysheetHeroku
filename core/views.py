from django.shortcuts import render
from shopping_cart.models import Order
from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    context = {
        'orders': orders
    }
    return render(request, "profile.html", context)
