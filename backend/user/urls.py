from django.urls import include, path
from rest_framework_nested import routers

from .views import userViewSet

router = routers.DefaultRouter()

router.register(r"users", userViewSet, basename="user")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
