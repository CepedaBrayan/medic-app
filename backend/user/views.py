from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from user.models import User

from .serializers import UserSerializer


class userViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def say_hello(self, request):
        # example for Andrea, response with code 200
        return HttpResponse("Hello World", status=200)
