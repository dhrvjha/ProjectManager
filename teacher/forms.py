from django import forms
from django.contrib.auth.forms import UserCreationForm

from teacher.models import Teacher


class TeacherRegisterForm(UserCreationForm):
    """Register user and update patients in signal"""

    email = forms.EmailField()

    class Meta:
        model = Teacher
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]
