from django.contrib import admin
from app.models import App, Developer, Reviewer, Language

# Register your models here.
admin.site.register(App)
admin.site.register(Developer)
admin.site.register(Reviewer)
admin.site.register(Language)
# admin.site.register(Device)