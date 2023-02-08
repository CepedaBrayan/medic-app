from rest_framework import serializers
from user.models import User


# create user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_admin",
            "is_staff",
        )
