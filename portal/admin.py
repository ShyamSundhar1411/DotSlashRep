from django.contrib import admin
from .models import ToDo,Profile,Note
# Register your models here.
admin.site.register(ToDo)
admin.site.register(Profile)
admin.site.register(Note)