from django.db import models
from django.urls import reverse


class Student(models.Model):
    """model for student"""

    registration_number = models.CharField(max_length=11, unique=True, primary_key=True)
    first_name = models.CharField(max_length=125, null=False, blank=False)
    last_name = models.CharField(max_length=125, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("student", kwargs={"pk": self.registration_number})


# class StudentsProject(models.Model):
#     uuid = models.UUIDField(default=uuid4, primary_key=True)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
