from django.contrib import admin

from .models import MenuLink, QuickLink

@admin.register(MenuLink)
class CpanelAdmin(admin.ModelAdmin):
    list_display =("Label", "Link", "BackButton")

@admin.register(QuickLink)
class CpanelAdmin(admin.ModelAdmin):
    list_display =("Label", "Link", "Icon", "BackButton")
