from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from user.models import UserAccountType


class IsSuperUser(BasePermission):
    message = "You are not a superuser."

    def has_permission(self, request: Request, view) -> bool:
        return bool(request.user and request.user.is_superuser)


class IsDoctor(BasePermission):
    message = "You are not a doctor."

    def has_permission(self, request: Request, view) -> bool:
        return bool(
            request.user and request.user.account_type == UserAccountType.DOCTOR.value
        )


class IsPatient(BasePermission):
    message = "You are not a patient."

    def has_permission(self, request: Request, view) -> bool:
        return bool(
            request.user and request.user.account_type == UserAccountType.PATIENT.value
        )


class IsStudent(BasePermission):
    message = "You are not a student."

    def has_permission(self, request: Request, view) -> bool:
        return bool(
            request.user and request.user.account_type == UserAccountType.STUDENT.value
        )
