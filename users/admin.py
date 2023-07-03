from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "nickname", "credit")
    search_fields = ("username", "nickname")
