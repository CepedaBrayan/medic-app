# import readonlypasswordhashfield
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from simple_history.admin import SimpleHistoryAdmin
from user.models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "account_type",
            "institutional_id",
            "first_name",
            "last_name",
            "dni",
            "birth_date",
            "phone_number",
            "address",
            "expiration_date",
            "is_active",
            "is_staff",
        )

        def save(self, commit=True):
            user = super().save(commit=False)
            if commit:
                user.save()
            return user


class UserCustom(SimpleHistoryAdmin, BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "account_type",
                    "institutional_id",
                    "first_name",
                    "last_name",
                    "dni",
                    "birth_date",
                    "phone_number",
                    "address",
                    "expiration_date",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    add_form = UserCreationForm
    list_display = [
        "email",
        "first_name",
        "last_name",
        "dni",
        "account_type",
        "date_joined",
    ]
    readonly_fields = ["is_active", "is_staff", "last_active"]
    ordering = ["email"]


admin.site.register(User, UserCustom)
