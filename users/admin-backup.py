from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    AdminPasswordChangeForm,
)
from django.utils.translation import gettext_lazy as _

from .models import LcOrderEmail, User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password", "RC_password")}),
        (_("Personal info"), {"fields": ("full_name", "revel_est_id", "company_name")}),
        (_("Permissions"), {"fields": ("is_active",),},),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "password1", "password2"),},
        ),
    )
    list_display = ("email", "full_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("email",)


@admin.register(LcOrderEmail)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("email",)
    ordering = ("-pk",)