from django.contrib import admin

from .models import SellingPoint


@admin.register(SellingPoint)
class SellingPointAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
