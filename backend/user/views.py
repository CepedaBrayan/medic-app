from django.http import HttpResponse
from django.shortcuts import render
from project.permissions import IsDoctor, IsPatient, IsStudent, IsSuperUser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from user.models import User

from .serializers import UserCreateSerializer, UserSelfUpdateSerializer, UserSerializer


class userViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    # methods list and delete just for superuser
    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsSuperUser]
        if self.action in ["list", "retrieve", "partial_update"]:
            self.permission_classes = [IsSuperUser | IsDoctor]
        return super(userViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ["create"]:
            return UserCreateSerializer
        # for endpoint my_profile use UserSelfUpdateSerializer
        if self.action in ["my_profile", "update_my_profile"]:
            return UserSelfUpdateSerializer
        return UserSerializer

    # disable put method
    def update(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    # endpoint for update password
    @action(detail=False, methods=["patch"])
    def update_my_password(self, request):
        user = request.user
        user.set_password(request.data["password"])
        user.save()
        return HttpResponse(status=204)

    # endpoint for see my profile
    @action(detail=False, methods=["get"])
    def my_profile(self, request):
        serializer = self.get_serializer_class()(request.user)
        return HttpResponse(serializer.data)

    # endpoint for update my profile
    @action(detail=False, methods=["patch"])
    def update_my_profile(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=204)
        return HttpResponse(serializer.errors, status=400)
