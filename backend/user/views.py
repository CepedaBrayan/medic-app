import json

from project.permissions import IsDoctor, IsPatient, IsStudent
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import Institution, User

from .serializers import (
    InstitutionSerializer,
    UserSelfUpdateSerializer,
    UserSerializer,
    UserUpdatePasswordSerializer,
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    # methods list and delete just for superuser
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsDoctor]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ["update_my_password"]:
            return UserUpdatePasswordSerializer
        if self.action in ["update_my_profile"]:
            return UserSelfUpdateSerializer
        return UserSerializer

    # endpoint for overwrite list method, just users with is_active = True
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    # endpoint for overwrite retrieve method, just users with is_active = True
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active is False:
            return Response(status=404)
        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)

    # endpoint for see my profile
    @action(detail=False, methods=["get"])
    def my_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.user)
        return Response(serializer.data)

    # endpoint for update my profile
    @action(detail=False, methods=["patch"])
    def update_my_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    # endpoint for update password
    @action(detail=False, methods=["patch"])
    def update_my_password(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated"}, status=200)
        return Response(serializer.errors, status=400)


class InstitutionViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]

    # endpoint for list all institutions with is_active = True
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    # endpoint for retrieve institution with is_active = True
    def retrieve(self, request, *args, **kwargs):
        institution = self.get_object()
        if institution.is_active is False:
            return Response(status=404)
        serializer = self.get_serializer_class()(institution)
        return Response(serializer.data)
