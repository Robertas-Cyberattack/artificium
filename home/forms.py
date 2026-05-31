from django import forms

from .models import (
    ClientProject,
    ProjectFile,
    ProjectMessage,
)


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


class ProjectMessageForm(forms.ModelForm):
    class Meta:
        model = ProjectMessage
        fields = [
            'message',
        ]


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = [
            'title',
            'file',
            'visible_to_client',
        ]