from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from projectrequest.models import ProjectRequest
from student.models import Student

# Create your views here.


class ProjectRequestView(View):
    model = Student
    postmodel = ProjectRequest

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.request: HttpRequest = None
        self.studentId = None

    def get_queryset(self):
        return self.model.get(registration_number=self.studentId)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["student_name"] = queryset.student_name
        context["registration_number"] = queryset.registration_number
        return context

    def get(self, request, studentId):
        self.request = request
        self.studentId = studentId
        return render(
            request, "projectrequest/registration.html", self.get_context_data()
        )

    def post(self, request):
        self.request = request
