from django.forms import ModelForm

from project.models import Project


class ProjectRegistrationForm(ModelForm):
    class Meta:
        model = Project
        fields = ("title", "description")
