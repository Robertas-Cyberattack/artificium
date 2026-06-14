from django.contrib import admin

from projects.models import (
    ClientProject,
    ProjectMessage,
    ProjectFile,
    Quote,
)

from payments.models import Invoice

admin.site.register(ClientProject)
admin.site.register(ProjectMessage)
admin.site.register(ProjectFile)
admin.site.register(Quote)
admin.site.register(Invoice)
