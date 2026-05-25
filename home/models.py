from django.contrib.auth.models import User
from django.db import models


class ClientProject(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

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

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title