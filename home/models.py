from django.contrib.auth.models import User
from django.db import models


class ClientProject(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('quoted', 'Quoted'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('paid', 'Paid'),
        ('in_progress', 'In Progress'),
        ('waiting_client', 'Waiting for Client'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=50, blank=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='requested'
    )
    progress = models.PositiveIntegerField(default=0)

    admin_notes = models.TextField(blank=True)
    client_notes = models.TextField(blank=True)

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProjectMessage(models.Model):
    project = models.ForeignKey(
        ClientProject,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()
    is_admin_message = models.BooleanField(default=False)

    is_read_by_admin = models.BooleanField(default=False)
    is_read_by_client = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message for {self.project.title}'


class ProjectFile(models.Model):
    project = models.ForeignKey(
        ClientProject,
        on_delete=models.CASCADE,
        related_name='files'
    )

    title = models.CharField(max_length=200)

    file = models.FileField(
        upload_to='project_files/'
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    visible_to_client = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Quote(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quotes'
    )

    project = models.ForeignKey(
        ClientProject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    reference = models.CharField(max_length=50, unique=True)
    service_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='requested'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    project = models.ForeignKey(
        ClientProject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='unpaid'
    )

    due_date = models.DateField(null=True, blank=True)

    pdf_file = models.FileField(
        upload_to='invoices/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number