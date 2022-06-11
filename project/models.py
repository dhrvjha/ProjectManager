from uuid import uuid4

from django.db import models

from student.models import Student
from teacher.models import Teacher


class Project(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    major_project_sorce_code = models.URLField(null=True, blank=True)
    minor_project_sorce_code = models.URLField(null=True, blank=True)
    major_project_presentation = models.URLField(null=True, blank=True)
    minor_project_presentation = models.URLField(null=True, blank=True)
    major_project_report = models.URLField(null=True, blank=True)
    minor_project_report = models.URLField(null=True, blank=True)

    is_approved = models.BooleanField(default=False, null=True, blank=True)
    date_posted = models.DateField(auto_now_add=True, null=True, blank=True)
    date_approved = models.DateField(null=True, blank=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
