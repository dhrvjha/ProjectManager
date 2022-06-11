import uuid

from django.db import models

from project.models import Project
from student.models import Student
from teacher.models import Teacher


class ProjectRequest(models.Model):
    uuid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
