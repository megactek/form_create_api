from django.contrib import admin
from .models import Form, FormInput, UserFormResponses

# Register your models here.
admin.site.register((Form, FormInput, UserFormResponses))
