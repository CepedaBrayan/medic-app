from django.urls import include, path
from rest_framework_nested import routers

from .views import InstitutionViewSet, UserViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"institutions", InstitutionViewSet, basename="institution")


urlpatterns = [
    path("api/v1/", include(router.urls)),
]
