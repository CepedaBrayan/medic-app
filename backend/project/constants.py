# import Integerchoices
from django.db.models import IntegerChoices


class UserAccountType(IntegerChoices):
    DOCTOR = 1, "Doctor"
    PATIENT = 2, "Patient"
    STUDENT = 3, "Student"
    OTHER = 4, "Other"
