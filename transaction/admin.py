from django.contrib import admin

from .models import Purchase, Reload


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("buyer", "seller", "article", "price", "date")
    list_filter = ("article", "date")
    search_fields = ("buyer__username", "buyer__nickname", "article__name")


@admin.register(Reload)
class ReloadAdmin(admin.ModelAdmin):
    list_display = ("buyer", "amount", "date")
    list_filter = ("date",)
    search_fields = ("buyer__username", "buyer__nickname")
