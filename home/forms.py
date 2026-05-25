from django import forms

from .models import ClientProject


class ClientProjectForm(forms.ModelForm):
    class Meta:
        model = ClientProject
        fields = [
            'client',
            'title',
            'description',
            'status',
            'progress',
            'admin_notes',
            'due_date',
        ]