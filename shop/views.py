import stripe
import json
import os
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http.response import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView
from stripe.api_resources import payment_intent

from home.models import Customer
from .models import Product, OrderItem, Address, StripePayment
from .utils import get_or_set_order_session
from .forms import AddToCartForm, AddressForm, StripePaymentForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(generic.ListView):
    template_name = 'shop/product_list.html'
    queryset=Product.objects.all()


class ProductDetailView(generic.FormView):
    template_name = 'shop/product_spotlight.html'
    form_class = AddToCartForm


    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("shop:summary") 

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs["product_id"] = self.get_object().id
        return kwargs
    
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object() 

        item_filter = order.items.filter(
            product=product,
            variety = form.cleaned_data['variety'])

        if item_filter.exists():
            item = item_filter.first()
            item.quantity = int(form.cleaned_data['quantity'])
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order    
            new_item.save()

        return super(ProductDetailView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class CartView(generic.TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context  

class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("shop:summary")   


class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("shop:summary") 


class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("shop:summary") 


class CheckoutView(generic.FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse("shop:stripe-pay")
    
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')
        selected_billing_address = form.cleaned_data.get('selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type='S',
                user = self.request.user,
                address_line_1=form.cleaned_data['shipping_address_line_1'],
                address_line_2=form.cleaned_data['shipping_address_line_2'],
                county=form.cleaned_data['shipping_address_county'],
                eircode=form.cleaned_data['shipping_address_eircode'],
            )
            order.shipping_address = address

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type='B',
                user = self.request.user,
                address_line_1=form.cleaned_data['billing_address_line_1'],
                address_line_2=form.cleaned_data['billing_address_line_2'],
                county=form.cleaned_data['billing_address_county'],
                eircode=form.cleaned_data['billing_address_eircode'],
            )
            order.billing_address = address
        order.save()

        messages.info(self.request, "Addresses have been added successfully")
        return super(CheckoutView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context 

class StripePaymentView(generic.FormView):
    template_name = 'shop/stripe_payment.html'
    form_class = StripePaymentForm

    def form_valid(self, form):
        payment_method = form.cleaned_data["selectedCard"]
        print(payment_method)
        if payment_method != "newCard":
            try:
                order = get_or_set_order_session(self.request)
                payment_intent = stripe.PaymentIntent.create(
                    amount=order.get_raw_total(),
                    currency='eur',
                    customer=self.request.user.customer.stripe_customer_id,
                    payment_method=payment_method,
                    off_session=True,
                    confirm=True,
                )
                payment_record, created = StripePayment.objects.get_or_create(
                    order=order
                )
                payment_record.payment_intent_id = payment_intent["id"]
                payment_record.amount = order.get_total()
                payment_record.save()


            except stripe.error.CardError as e:
                err = e.error
                # Error code will be authentication_required if authentication is needed
                print("Code is: %s" % err.code)
                payment_intent_id = err.payment_intent['id']
                payment_intent = stripe.PaymentIntent.retrieve(
                    payment_intent_id)
                messages.warning(self.request, "Code is: %s" % err.code)
        return redirect("/")

    def get_context_data(self, **kwargs):
        user = self.request.user
        if not user.customer.stripe_customer_id:
            stripe_customer = stripe.Customer.create(email=user.email)
            user.customer.stripe_customer_id = stripe_customer["id"]
            user.customer.save()

        order = get_or_set_order_session(self.request)

        payment_intent = stripe.PaymentIntent.create(
            amount=order.get_raw_total(), #Amount in cents
            currency='eur',
            customer=user.customer.stripe_customer_id,
        )
        print(payment_intent)
        payment_record, created = StripePayment.objects.get_or_create(
            order=order
        )
        payment_record.payment_intent_id = payment_intent["id"]
        payment_record.amount = order.get_total()
        payment_record.save()

        cards = stripe.PaymentMethod.list(
            customer=user.customer.stripe_customer_id,
            type="card",
        )
        pay_methods=[]
        for card in cards:
            pay_methods.append(card["id"])

        print(cards)

        context = super(StripePaymentView, self).get_context_data(**kwargs)
        context ["order"] = get_or_set_order_session(self.request)
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        context["client_secret"] = payment_intent["client_secret"]
        context["payment_methods"] = pay_methods
        return context

@csrf_exempt
def stripe_webhook_view(request):
    endpoint_secret = settings.STRIPE_WH_SECRET_SHOP
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        stripe_payment = StripePayment.objects.get(
            payment_intent_id=payment_intent["id"],
        )
        stripe_payment.successful = True
        stripe_payment.save()
        order = stripe_payment.order
        order.ordered = True
        order.ordered_date = timezone.now()
        order.save()

        handle_receipt(payment_intent)
    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)

def handle_receipt(payment_intent):
    User = get_user_model()
    # Modified from Donations app
    customer_id = payment_intent["customer"]
    customer_user = Customer.objects.get(stripe_customer_id=customer_id)
    customer_user_email = customer_user.email
    receipt_link = payment_intent["receipt_url"]
    purchase_amount = payment_intent["amount"]
    display_amount_display = "{0:.2f}".format(purchase_amount / 100)
    send_mail('Thank you for your purchase', f'Hi there {customer_user}, thanks for purchasing trees from Citizen Tree. View receipt here: {receipt_link}', 
        'ms4.citizentree@gmail.com', [customer_user_email], fail_silently=False)

    # payment_intent = session.get("payment_intent") 