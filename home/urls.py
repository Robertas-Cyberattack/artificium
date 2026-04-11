from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('services/', views.services, name='services'),
    path('request-quote/', views.request_quote, name='request_quote'),
    path('pay-quote/', views.pay_quote, name='pay_quote'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('contact/', views.contact, name='contact'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]