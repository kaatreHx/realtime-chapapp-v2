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

@admin.register(models.UserChat)
class UserChatAdmin(admin.ModelAdmin):
    list_display = (
        'user_sender',
        'user_receiver',
        'message',
        'timestamp'
    )