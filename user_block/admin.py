from django.contrib import admin

from .models import UserBlock


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    pass


