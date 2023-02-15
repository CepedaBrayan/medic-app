# import readonlypasswordhashfield
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from simple_history.admin import SimpleHistoryAdmin
from user.models import Institution, User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
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
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserCustom(SimpleHistoryAdmin, BaseUserAdmin):
    fieldsets = (
        (
            ("Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            ("Personal info"),
            {
                "fields": (
                    "account_type",
                    "institution",
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
                "fields": ("is_superuser",),
            },
        ),
    )
    add_fieldsets = (
        (
            ("Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            ("Personal info"),
            {
                "fields": (
                    "account_type",
                    "institution",
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
                "fields": ("is_superuser",),
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
    readonly_fields = ["last_active"]
    ordering = ["email"]


admin.site.register(User, UserCustom)
admin.site.register(Institution)
