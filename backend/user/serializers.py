from rest_framework import serializers
from user.models import User


# create user serializer
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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "dni",
            "account_type",
        )
        read_only_fields = ("id",)

    # create user hashing password
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSelfUpdateSerializer(serializers.ModelSerializer):
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
        read_only_fields = (
            "id",
            "account_type",
            "expiration_date",
            "is_active",
            "is_staff",
            "last_active",
        )
