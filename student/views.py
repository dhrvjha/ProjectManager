from typing import Any, Dict

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from project.forms import ProjectRegistrationForm
from project.models import Project
from projectrequest.models import ProjectRequest
from student.forms import StudentApplyForm
from student.models import Student
from teacher.models import Teacher


class StudentRequestView(View):
    form = StudentApplyForm()
    template_name = "student/registration.html"
    model = Student
    success_template_name = "student/registration_success.html"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.request: HttpRequest

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = {}
        context["studentform"] = StudentApplyForm(self.request.POST)
        context["projectform"] = ProjectRegistrationForm(self.request.POST)
        context["teachers"] = Teacher.objects.all()
        return context

    def get_queryset(self, **kwargs):
        return None

    def get(self, request):
        self.request = request
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        self.request = request
        studentform = StudentApplyForm(request.POST)
        projectform = ProjectRegistrationForm(request.POST)
        teacherId = request.POST.get("teacher")
        try:
            teacher = Teacher.objects.get(id=teacherId)
        except Teacher.DoesNotExist:
            print("teacher does not exist")
            return render(request, self.template_name, self.get_context_data())
        reg_no = studentform.data.get("registration_number")

        if studentform.is_valid() and projectform.is_valid():
            student = studentform.save()
            title = projectform.cleaned_data.get("title")
            description = projectform.cleaned_data.get("description")
            project = Project(
                title=title, description=description, teacher=teacher, student=student
            )
            project.save()
            ProjectRequest(student=student, teacher=teacher, project=project).save()
        elif Student.objects.filter(registration_number=reg_no).exists():
            return redirect("student_status", studentId=reg_no)
        else:
            return render(request, self.template_name, self.get_context_data())

        return render(request, self.success_template_name)


class StudentApplicationStatusView(View):
    template_name = "student/status.html"
    form_template_name = "student/status.html"
    model = ProjectRequest

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.request: HttpRequest
        self.studentId: str

    def get_queryset(self):
        student = Student.objects.get(registration_number=self.studentId)
        return Project.objects.filter(student=student).first()

    def get_context_data(self, **kwargs):
        context = {}
        queryset = self.get_queryset()
        if queryset is None:
            raise Project.DoesNotExist()
        context["student_name"] = str(queryset.student)
        context["registration_number"] = queryset.student.registration_number
        context["is_approved"] = queryset.is_approved
        context["rejected"] = False
        return context

    def get(self, request, studentId):
        self.studentId = studentId
        try:
            context = self.get_context_data()
        except Student.DoesNotExist or Project.DoesNotExist:
            return render(request, self.template_name, {"rejected": True})
        return render(request, self.template_name, context)
