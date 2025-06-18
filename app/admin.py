from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
        'is_active',
        'online_status'
    )