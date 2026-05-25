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

    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    path('dashboard/quotes/', views.my_quotes, name='my_quotes'),
    path('dashboard/payments/', views.my_payments, name='my_payments'),
]