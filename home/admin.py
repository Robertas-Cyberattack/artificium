from django.contrib import admin

from .models import (
    ClientProject,
    ProjectFile,
    ProjectMessage,
)


admin.site.register(ClientProject)
admin.site.register(ProjectMessage)
admin.site.register(ProjectFile)