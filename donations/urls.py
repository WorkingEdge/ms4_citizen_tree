from django.urls import path
from . import views
from .views import (DonateLandingPage,
                    CancelView,
                    SuccessView,
                    CreateCheckoutSessionView, 
                    stripe_webhook
                    )


app_name = 'donations'

urlpatterns = [
    path('', DonateLandingPage.as_view(), name="donate-landing"),
    #path('donations/create-checkout-session/', views.create_checkout_session, name ="create-checkout-session"),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhooks/stripe', stripe_webhook, name='stripe-webhook'),
]