from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('services/', views.services, name='services'),
    path('request-quote/', views.request_quote, name='request_quote'),
    path('pay-quote/', views.pay_quote, name='pay_quote'),
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

    # ADMIN PROJECTS
    path('dashboard/admin/projects/', views.admin_projects, name='admin_projects'),
    path('dashboard/admin/projects/create/', views.admin_create_project, name='admin_create_project'),

    path(
        'dashboard/admin/projects/<int:project_id>/',
        views.admin_project_detail,
        name='admin_project_detail'
    ),

    path(
        'dashboard/admin/projects/<int:project_id>/edit/',
        views.admin_edit_project,
        name='admin_edit_project'
    ),

    path(
        'dashboard/admin/projects/<int:project_id>/delete/',
        views.admin_delete_project,
        name='admin_delete_project'
    ),

    path(
        'dashboard/admin/projects/<int:project_id>/messages/',
        views.admin_project_messages,
        name='admin_project_messages'
    ),

    # ADMIN CLIENTS
    path(
        'dashboard/admin/clients/',
        views.admin_clients,
        name='admin_clients'
    ),

    path(
        'dashboard/admin/clients/create/',
        views.admin_create_client,
        name='admin_create_client'
    ),

    path(
        'dashboard/admin/clients/<int:client_id>/edit/',
        views.admin_edit_client,
        name='admin_edit_client'
    ),

    path(
        'dashboard/admin/clients/<int:client_id>/delete/',
        views.admin_delete_client,
        name='admin_delete_client'
    ),

    # CLIENT PROJECTS
    path(
        'dashboard/projects/create/',
        views.client_create_project,
        name='client_create_project'
    ),

    path(
        'dashboard/projects/<int:project_id>/edit/',
        views.client_edit_project,
        name='client_edit_project'
    ),

    path(
        'dashboard/projects/<int:project_id>/delete/',
        views.client_delete_project,
        name='client_delete_project'
    ),

    path(
        'dashboard/projects/<int:project_id>/pay/',
        views.create_project_payment,
        name='create_project_payment'
    ),


    path(
    'dashboard/projects/<int:project_id>/invoice/',
    views.download_invoice,
    name='download_invoice'
    ),

    path(
        'dashboard/projects/<int:project_id>/messages/',
        views.client_project_messages,
        name='client_project_messages'
    ),

    # CLIENT MESSAGE EDIT / DELETE
    path(
        'dashboard/messages/<int:message_id>/edit/',
        views.client_edit_message,
        name='client_edit_message'
    ),

    path(
        'dashboard/messages/<int:message_id>/delete/',
        views.client_delete_message,
        name='client_delete_message'
    ),

    # ADMIN MESSAGE EDIT / DELETE
    path(
        'dashboard/admin/messages/<int:message_id>/edit/',
        views.admin_edit_message,
        name='admin_edit_message'
    ),

    path(
        'dashboard/admin/messages/<int:message_id>/delete/',
        views.admin_delete_message,
        name='admin_delete_message'
    ),
]