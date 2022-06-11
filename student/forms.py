from django.forms import ModelForm

from student.models import Student


class StudentApplyForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    # def is_valid():
    #     return super().is_valid()
