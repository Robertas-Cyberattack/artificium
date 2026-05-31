from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    ClientProject,
    ProjectFile,
    ProjectMessage,
)

import stripe


def index(request):
    return render(request, 'home/index.html')


def services(request):
    return render(request, 'home/services.html')


def request_quote(request):
    submitted = False

    if request.method == 'POST':
        submitted = True

    return render(
        request,
        'home/request_quote.html',
        {'submitted': submitted},
    )


def contact(request):
    submitted = False

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not full_name or not email or not subject or not message:
            messages.error(request, 'Please complete all required fields.')
            return redirect('contact')

        email_subject = f'Artificium Contact Form: {subject}'
        email_message = (
            f'Full Name: {full_name}\n'
            f'Company Name: {company_name}\n'
            f'Email: {email}\n'
            f'Phone Number: {phone_number}\n\n'
            f'Message:\n{message}'
        )

        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        submitted = True

    return render(
        request,
        'home/contact.html',
        {'submitted': submitted},
    )


def pay_quote(request):
    return render(
        request,
        'home/pay_quote.html',
        {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        },
    )


def create_checkout_session(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method.')

    quote_reference = request.POST.get('quote_reference', '').strip().upper()
    client_name = request.POST.get('client_name', '').strip()
    client_email = request.POST.get('client_email', '').strip()
    service_name = request.POST.get('service_name', '').strip()
    quote_amount = request.POST.get('quote_amount', '').strip()

    if not quote_reference or not client_email or not service_name or not quote_amount:
        messages.error(request, 'Please complete all required payment fields.')
        return redirect('pay_quote')

    try:
        amount_decimal = Decimal(quote_amount)
    except InvalidOperation:
        messages.error(request, 'Enter a valid quote amount.')
        return redirect('pay_quote')

    if amount_decimal <= 0:
        messages.error(request, 'Quote amount must be greater than zero.')
        return redirect('pay_quote')

    amount_in_pence = int(amount_decimal * 100)

    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, 'Stripe is not configured yet. Add your Stripe keys first.')
        return redirect('pay_quote')

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            mode='payment',
            success_url=f"{settings.DOMAIN}/payment-success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.DOMAIN}/payment-cancel/",
            client_reference_id=quote_reference,
            customer_email=client_email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': f'{service_name} Quote Payment',
                            'description': f'Quote reference: {quote_reference}',
                        },
                        'unit_amount': amount_in_pence,
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                'quote_reference': quote_reference,
                'client_name': client_name,
                'client_email': client_email,
                'service_name': service_name,
                'quote_amount': str(amount_decimal),
            },
        )
        return redirect(checkout_session.url, code=303)

    except Exception as error:
        messages.error(request, f'Unable to start payment session: {error}')
        return redirect('pay_quote')


def payment_success(request):
    session_id = request.GET.get('session_id')
    session = None

    if session_id and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception:
            session = None

    return render(
        request,
        'home/payment_success.html',
        {
            'session': session,
        },
    )


def payment_cancel(request):
    return render(request, 'home/payment_cancel.html')

def terms(request):
    return render(request, 'legal/terms.html')


def privacy(request):
    return render(request, 'legal/privacy.html')

@login_required
def dashboard(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')

    projects = ClientProject.objects.filter(
        client=request.user
    ).order_by('-created_at')

    return render(
        request,
        'home/dashboard.html',
        {
            'projects': projects,
        }
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    clients = User.objects.filter(
        is_staff=False
    )

    projects = ClientProject.objects.all().order_by(
        '-created_at'
    )

    messages = ProjectMessage.objects.all().order_by(
        '-created_at'
    )[:10]

    files = ProjectFile.objects.all().order_by(
        '-uploaded_at'
    )[:10]

    return render(
        request,
        'home/admin_dashboard.html',
        {
            'clients': clients,
            'projects': projects,
            'messages': messages,
            'files': files,
        }
    )

@login_required
def my_quotes(request):
    return render(request, 'home/my_quotes.html')


@login_required
def my_payments(request):
    return render(request, 'home/my_payments.html')

@login_required
def admin_projects(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    projects = ClientProject.objects.all().order_by('-created_at')

    return render(
        request,
        'home/admin_projects.html',
        {
            'projects': projects,
        }
    )

@login_required
def admin_create_project(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    clients = User.objects.filter(
        is_staff=False
    )

    if request.method == 'POST':

        client_id = request.POST.get('client')
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        progress = request.POST.get('progress') or 0

        client = User.objects.get(
            id=client_id
        )

        ClientProject.objects.create(
            client=client,
            title=title,
            description=description,
            status=status,
            progress=progress,
        )

        messages.success(
            request,
            'Project created successfully.'
        )

        return redirect('admin_projects')

    return render(
        request,
        'home/admin_create_project.html',
        {
            'clients': clients,
            'status_choices': ClientProject.STATUS_CHOICES,
        }
    )

@login_required
def admin_project_detail(request, project_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    project = ClientProject.objects.get(id=project_id)

    return render(request, 'home/admin_project_detail.html', {
        'project': project,
    })


@login_required
def admin_edit_project(request, project_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    project = ClientProject.objects.get(id=project_id)
    clients = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        project.client = User.objects.get(id=request.POST.get('client'))
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.status = request.POST.get('status')
        project.progress = request.POST.get('progress') or 0
        project.admin_notes = request.POST.get('admin_notes')
        project.save()

        messages.success(request, 'Project updated successfully.')
        return redirect('admin_project_detail', project_id=project.id)

    return render(request, 'home/admin_edit_project.html', {
        'project': project,
        'clients': clients,
        'status_choices': ClientProject.STATUS_CHOICES,
    })


@login_required
def admin_create_project(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    clients = User.objects.filter(is_staff=False)

    if request.method == 'POST':

        existing_client_id = request.POST.get('existing_client')
        new_client_username = request.POST.get('new_client_username', '').strip()
        new_client_email = request.POST.get('new_client_email', '').strip()

        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        progress = request.POST.get('progress') or 0

        if existing_client_id:
            client = User.objects.get(id=existing_client_id)
        else:
            if not new_client_username or not new_client_email:
                messages.error(request, 'Select existing client or create a new client.')
                return redirect('admin_create_project')

            client = User.objects.create_user(
                username=new_client_username,
                email=new_client_email,
                password='TemporaryPassword123!'
            )

        ClientProject.objects.create(
            client=client,
            title=title,
            description=description,
            status=status,
            progress=progress,
        )

        messages.success(request, 'Project created successfully.')
        return redirect('admin_projects')

    return render(
        request,
        'home/admin_create_project.html',
        {
            'clients': clients,
            'status_choices': ClientProject.STATUS_CHOICES,
        }
    )