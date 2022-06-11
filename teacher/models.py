from django.contrib.auth.models import AbstractUser
from django.db import models


class Teacher(AbstractUser):
    """Model for teachers"""

    class DepartmentChoices(models.TextChoices):
        # Todo: list all the departments
        CSE = "0", "Compuer Science"
        IT = "1", "Information Technology"

    department = models.TextField(
        choices=DepartmentChoices.choices, null=False, blank=False
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
