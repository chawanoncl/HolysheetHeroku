from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Sheet, Page
from shopping_cart.models import Order, OrderItem

OWNED = 'owned'
IN_CART = 'in_cart'
NOT_IN_CART = 'not_in_cart'

def check_sheet_relationship(request, sheet):
    if sheet in request.user.userlibrary.sheets.all():
        return OWNED
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item_qs = OrderItem.objects.filter(sheet=sheet)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item in order.items.all():
                return IN_CART
    return NOT_IN_CART

def sheet_list(request):
    queryset = Sheet.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, "sheet_list.html", context)




@login_required
def sheet_detail(request, slug):
    sheet = get_object_or_404(Sheet, slug=slug)
    sheet_status = check_sheet_relationship(request, sheet)
    context = {
        'sheet': sheet,
        'sheet_status': sheet_status
    }
    return render(request, "sheet_detail.html", context)


def page_detail(request, sheet_slug, page_number):
    page_qs = Page.objects \
        .filter(sheet__slug=sheet_slug) \
        .filter(page_number=page_number)

    page = page_qs[0]
    sheet_status = check_sheet_relationship(request, page.sheet)

    if page_qs.exists():
        context = {
            'page': page,
            'sheet_status': sheet_status
        }
        return render(request, "page_detail.html", context)
    raise Http404
