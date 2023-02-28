from rest_framework import serializers
from user.models import Institution, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
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
            "last_active",
        )
        read_only_fields = ("id", "is_active", "is_staff", "last_active")


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "password", "new_password")
        read_only_fields = ("id",)

    # update user password
    def update(self, instance, validated_data):
        if instance.check_password(validated_data["password"]):
            instance.set_password(validated_data["new_password"])
            instance.save()
            return instance


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            "id",
            "name",
            "address",
            "phone_number",
            "email",
            "is_active",
        )
        read_only_fields = ("id", "is_active")

    # create institution
    def create(self, validated_data):
        institution = Institution.objects.create(**validated_data)
        return institution
