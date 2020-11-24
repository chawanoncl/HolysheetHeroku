from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from sheets.models import Sheet
from .models import Order, OrderItem, Payment
import string
import stripe
import random
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))


@login_required
def add_to_cart(request, sheet_slug):
    sheet = get_object_or_404(Sheet, slug=sheet_slug)
    order_item, created = OrderItem.objects.get_or_create(sheet=sheet)
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()
    messages.info(request, "Item successfully added to your cart.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, sheet_slug):
    sheet = get_object_or_404(Sheet, slug=sheet_slug)
    order_item = get_object_or_404(OrderItem, sheet=sheet)
    order = get_object_or_404(Order, user=request.user)
    order.items.remove(order_item)
    order.save()
    messages.info(request, "Item successfully removed to your cart.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def order_view(request):
    order = get_object_or_404(Order, user=request.user)
    context = {
        'order': order
    }
    return render(request, "order_summary.html", context)


@login_required
def checkout(request):
    order = get_object_or_404(Order, user=request.user)
    if request.method == "POST":

        try:
            order.ref_code = create_ref_code()
            token = request.POST.get('stripeToken')
            charge = stripe.Charge.create(
                amount=int(order.get_total() * 100),
                currency="usd",
                source=token,
                description="Charge for {request.user.username}",
            )

            payment = Payment()
            payment.order = order
            payment.stripe_charge_id = charge.id
            payment.total_amount = order.get_total()
            payment.save()

            sheets = [item.sheet for item in order.items.all()]
            for sheet in sheets:
                request.user.userlibrary.sheets.add(sheet)
        
            order.is_ordered = True
            order.save()

            return redirect("/account/profile/")

        except stripe.error.CardError as e:
            message.error(request, "There was a card error.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.RateLimitError as e:
            message.error(request, "There was a rate limit on Stripe.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.InvalidRequestError as e:
            message.error(request, "Invalid parameters for Stripe request.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.AuthenticationError as e:
            message.error(request, "Invalid Stripe API key.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.APIConnectionError as e:
            message.error(request, "There was a network error. Please try again.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.StripeError as e:
            message.error(request, "There was an error. Please try again.")
            return redirect(reverse("cart:checkout"))
        except Exception as e:
            message.error(request, "There was a serious error.")
            return redirect(reverse("cart:checkout"))

        

    context = {
        'order': order}

    return render(request, "checkout.html", context)
