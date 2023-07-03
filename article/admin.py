from django.contrib import admin

from .models import Article, Category, Foundation, Period, Price


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name", "foundation__name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Foundation)
class FoundationAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "mail")
    search_fields = ("name", "website", "mail")


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("article", "foundation", "period", "group", "amount")
    list_filter = ("article", "foundation", "period", "group")
    search_fields = (
        "article__name",
        "foundation__name",
        "period__name",
        "group__name",
    )


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("name", "start", "end")
    search_fields = ("name",)
