from decimal import Decimal, InvalidOperation

import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from .models import ClientProject, ProjectFile, ProjectMessage


def index(request):
    return render(request, 'home/index.html')


def services(request):
    return render(request, 'home/services.html')


def request_quote(request):
    submitted = False

    if request.method == 'POST':
        submitted = True

    return render(request, 'home/request_quote.html', {'submitted': submitted})


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

    return render(request, 'home/contact.html', {'submitted': submitted})


def pay_quote(request):
    return render(
        request,
        'home/pay_quote.html',
        {'stripe_public_key': settings.STRIPE_PUBLIC_KEY},
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


@login_required
def create_project_payment(request, project_id):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    project = get_object_or_404(
        ClientProject,
        id=project_id,
        client=request.user,
    )

    if project.price <= 0:
        messages.error(request, 'This project does not have a payment amount yet.')
        return redirect('dashboard')

    if project.is_paid:
        messages.info(request, 'This project has already been paid.')
        return redirect('dashboard')

    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, 'Stripe is not configured yet.')
        return redirect('dashboard')

    stripe.api_key = settings.STRIPE_SECRET_KEY

    amount_in_pence = int(project.price * 100)

    try:
        checkout_session = stripe.checkout.Session.create(
            mode='payment',
            success_url=f"{settings.DOMAIN}/payment-success/?session_id={{CHECKOUT_SESSION_ID}}&project_id={project.id}",
            cancel_url=f"{settings.DOMAIN}/dashboard/",
            client_reference_id=f'PROJECT-{project.id}',
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': project.title,
                            'description': f'Project invoice: {project.invoice_number}',
                        },
                        'unit_amount': amount_in_pence,
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                'project_id': project.id,
                'client_username': request.user.username,
                'invoice_number': project.invoice_number,
                'project_title': project.title,
            },
        )

        return redirect(checkout_session.url, code=303)

    except Exception as error:
        messages.error(request, f'Unable to start payment session: {error}')
        return redirect('dashboard')


def payment_success(request):
    session_id = request.GET.get('session_id')
    project_id = request.GET.get('project_id')
    session = None

    if session_id and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            session = stripe.checkout.Session.retrieve(session_id)

            if project_id:
                project = ClientProject.objects.filter(id=project_id).first()

                if project:
                    project.is_paid = True
                    project.status = 'paid'
                    project.save()

        except Exception:
            session = None

    return render(request, 'home/payment_success.html', {'session': session})


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

    return render(request, 'home/dashboard.html', {'projects': projects})


@login_required
def client_create_project(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        client_notes = request.POST.get('client_notes', '').strip()

        if not title:
            messages.error(request, 'Please enter project title.')
            return redirect('client_create_project')

        ClientProject.objects.create(
            client=request.user,
            title=title,
            description=description,
            client_notes=client_notes,
            status='requested',
            price=0,
            is_paid=False,
            progress=0,
        )

        messages.success(request, 'Project request submitted successfully.')
        return redirect('dashboard')

    return render(request, 'home/client_create_project.html')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    clients = User.objects.filter(is_staff=False)
    projects = ClientProject.objects.all().order_by('-created_at')
    recent_messages = ProjectMessage.objects.all().order_by('-created_at')[:10]
    files = ProjectFile.objects.all().order_by('-uploaded_at')[:10]

    return render(
        request,
        'home/admin_dashboard.html',
        {
            'clients': clients,
            'projects': projects,
            'messages': recent_messages,
            'files': files,
        },
    )


@login_required
def my_quotes(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    projects = ClientProject.objects.filter(
        client=request.user
    ).order_by('-created_at')

    return render(request, 'home/my_quotes.html', {'projects': projects})


@login_required
def my_payments(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    projects = ClientProject.objects.filter(
        client=request.user
    ).order_by('-created_at')

    return render(request, 'home/my_payments.html', {'projects': projects})


@login_required
def admin_projects(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    projects = ClientProject.objects.all().order_by('-created_at')

    return render(request, 'home/admin_projects.html', {'projects': projects})


@login_required
def admin_create_project(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    clients = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        existing_client_id = request.POST.get('existing_client')
        new_client_username = request.POST.get('new_client_username', '').strip()
        new_client_email = request.POST.get('new_client_email', '').strip()

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price') or 0
        invoice_number = request.POST.get('invoice_number', '').strip()
        status = request.POST.get('status', 'requested')
        progress = request.POST.get('progress') or 0

        if existing_client_id:
            client = get_object_or_404(User, id=existing_client_id)
        else:
            if not new_client_username or not new_client_email:
                messages.error(request, 'Select existing client or create a new client.')
                return redirect('admin_create_project')

            client = User.objects.create_user(
                username=new_client_username,
                email=new_client_email,
                password='TemporaryPassword123!',
            )

        ClientProject.objects.create(
            client=client,
            title=title,
            description=description,
            price=price,
            invoice_number=invoice_number,
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
        },
    )


@login_required
def admin_project_detail(request, project_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    project = get_object_or_404(ClientProject, id=project_id)

    return render(request, 'home/admin_project_detail.html', {'project': project})


@login_required
def admin_edit_project(request, project_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    project = get_object_or_404(ClientProject, id=project_id)
    clients = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        project.client = get_object_or_404(User, id=request.POST.get('client'))
        project.title = request.POST.get('title', '').strip()
        project.description = request.POST.get('description', '').strip()
        project.price = request.POST.get('price') or 0
        project.invoice_number = request.POST.get('invoice_number', '').strip()
        project.is_paid = request.POST.get('is_paid') == 'on'
        project.status = request.POST.get('status', 'requested')
        project.progress = request.POST.get('progress') or 0
        project.admin_notes = request.POST.get('admin_notes', '').strip()
        project.save()

        messages.success(request, 'Project updated successfully.')
        return redirect('admin_project_detail', project_id=project.id)

    return render(
        request,
        'home/admin_edit_project.html',
        {
            'project': project,
            'clients': clients,
            'status_choices': ClientProject.STATUS_CHOICES,
        },
    )


@login_required
def admin_delete_project(request, project_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    project = get_object_or_404(ClientProject, id=project_id)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('admin_projects')

    return render(request, 'home/admin_delete_project.html', {'project': project})


@login_required
def admin_clients(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    clients = User.objects.filter(is_staff=False).order_by('-date_joined')

    return render(request, 'home/admin_clients.html', {'clients': clients})


@login_required
def admin_create_client(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not email or not password:
            messages.error(request, 'Please complete all fields.')
            return redirect('admin_create_client')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        messages.success(request, 'Client created successfully.')
        return redirect('admin_clients')

    return render(request, 'home/admin_client_form.html', {
        'page_title': 'Create Client',
        'client': None,
    })


@login_required
def admin_edit_client(request, client_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    client = get_object_or_404(User, id=client_id, is_staff=False)

    if request.method == 'POST':
        client.username = request.POST.get('username', '').strip()
        client.email = request.POST.get('email', '').strip()
        client.is_active = request.POST.get('is_active') == 'on'

        password = request.POST.get('password', '').strip()
        if password:
            client.set_password(password)

        client.save()

        messages.success(request, 'Client updated successfully.')
        return redirect('admin_clients')

    return render(request, 'home/admin_client_form.html', {
        'page_title': 'Edit Client',
        'client': client,
    })


@login_required
def admin_delete_client(request, client_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    client = get_object_or_404(User, id=client_id, is_staff=False)

    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('admin_clients')

    return render(request, 'home/admin_delete_client.html', {'client': client})


@login_required
def client_edit_project(request, project_id):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    project = get_object_or_404(
        ClientProject,
        id=project_id,
        client=request.user,
    )

    if project.is_paid or project.status not in ['requested']:
        messages.error(request, 'You can only edit projects before they are quoted or paid.')
        return redirect('dashboard')

    if request.method == 'POST':
        project.title = request.POST.get('title', '').strip()
        project.description = request.POST.get('description', '').strip()
        project.client_notes = request.POST.get('client_notes', '').strip()
        project.save()

        messages.success(request, 'Project updated successfully.')
        return redirect('dashboard')

    return render(request, 'home/client_edit_project.html', {
        'project': project,
    })


@login_required
def client_delete_project(request, project_id):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    project = get_object_or_404(
        ClientProject,
        id=project_id,
        client=request.user,
    )

    if project.is_paid or project.status not in ['requested']:
        messages.error(request, 'You can only delete projects before they are quoted or paid.')
        return redirect('dashboard')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('dashboard')

    return render(request, 'home/client_delete_project.html', {
        'project': project,
    })


@login_required
def client_project_messages(request, project_id):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    project = get_object_or_404(
        ClientProject,
        id=project_id,
        client=request.user,
    )

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()

        if message_text:
            ProjectMessage.objects.create(
                project=project,
                sender=request.user,
                message=message_text,
                is_admin_message=False,
            )
            messages.success(request, 'Message sent successfully.')

        return redirect('client_project_messages', project_id=project.id)

    project_messages = project.messages.all().order_by('created_at')

    return render(request, 'home/client_project_messages.html', {
        'project': project,
        'project_messages': project_messages,
    })


@login_required
def admin_project_messages(request, project_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    project = get_object_or_404(ClientProject, id=project_id)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()

        if message_text:
            ProjectMessage.objects.create(
                project=project,
                sender=request.user,
                message=message_text,
                is_admin_message=True,
            )
            messages.success(request, 'Message sent successfully.')

        return redirect('admin_project_messages', project_id=project.id)

    project_messages = project.messages.all().order_by('created_at')

    return render(request, 'home/admin_project_messages.html', {
        'project': project,
        'project_messages': project_messages,
    })