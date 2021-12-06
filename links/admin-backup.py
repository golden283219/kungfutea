from django.contrib import admin

from .models import SopAndPosLink

@admin.register(SopAndPosLink)
class CpanelAdmin(admin.ModelAdmin):
    list_display =("SOP_link", "POS_link")

# admin.site.register(SopAndPosLink)