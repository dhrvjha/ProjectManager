import uuid

from django.contrib import messages
from django.db import models
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import View

from project.models import Project
from projectrequest.models import ProjectRequest
from teacher.forms import TeacherRegisterForm


class ProjectRequestView(View):
    model: models.Model = ProjectRequest
    paginate_by = 10
    template_name = "teacher/list_requests.html"
    allow_empty = True

    def get_queryset(self):
        return self.model.objects.filter(teacher=self.request.user)

    def get_context_data(self, **kwargs):
        self.request = kwargs["request"]
        context = {}
        project_requests = self.get_queryset()
        context["requests"] = [
            {
                "student_name": str(proj_req.student),
                "registration_number": proj_req.student.registration_number,
                "project_title": proj_req.project.title,
                "project_description": proj_req.project.description,
                "project_uuid": str(proj_req.uuid),
            }
            for proj_req in project_requests
        ]
        return context

    def get(self, request):
        context = self.get_context_data(request=request)
        return render(request, self.template_name, context)


class ProjectRequestDetailView(View):

    template_name = "teacher/project_request_details.html"

    def __init__(self):
        super().__init__()
        self.request: HttpRequest
        self.projectRequestId: uuid

    def get_context_data(self, **kwargs):
        context = {}
        project_request = self.get_queryset()
        context["requests"] = {
            "student_name": str(project_request.student),
            "registration_number": project_request.student.registration_number,
            "project_title": project_request.project.title,
            "project_description": project_request.project.description,
        }
        return context

    def get_queryset(self) -> ProjectRequest:
        return ProjectRequest.objects.select_related("project", "student").get(
            uuid=self.projectRequestId
        )

    def get(self, request, projectRequestId):
        self.request = request
        self.projectRequestId = projectRequestId
        try:
            context = self.get_context_data()
        except ProjectRequest.DoesNotExist:
            return HttpResponseNotFound("Requested page was not found!")
        return render(request, self.template_name, context)

    def post(self, request, projectRequestId):
        self.projectRequestId = projectRequestId
        self.request = request
        try:
            projectrequest = self.get_queryset()
        except ProjectRequest.DoesNotExist:
            return HttpResponseNotFound("Requested page was not found!")
        if request.POST.get("approval") == "True":
            projectrequest.project.is_approved = True
            projectrequest.project.save()
            projectrequest.delete()
        else:
            projectrequest.student.delete()
        return redirect("project_request_view")


class ProjectsView(View):
    model = Project
    template_name = "teacher/list_projects.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.request = kwargs["request"]
        context = {}
        project_requests = self.get_queryset()
        context["requests"] = [
            {
                "student_name": str(proj_req.student),
                "registration_number": proj_req.student.registation_number,
                "project_title": proj_req.project.title,
                "project_description": proj_req.project.description,
            }
            for proj_req in project_requests
        ]
        return context

    def get_queryset(self):
        return self.model.objects.filter(teacher=self.request.user, is_approved=True)

    def get(self, request):
        context = self.get_context_data(request=request)
        return render(request, self.template_name, context)


class TeacherHomeView(View):
    def get(self, request):
        return render(request, "teacher/home.html")


class RegisterTeacher(View):
    def get(self, request: HttpRequest):
        context = {"form": TeacherRegisterForm()}
        return render(request, "teacher/register.html", context)

    def post(self, request: HttpRequest):
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for { username }!")
            return redirect("patient_home")
        else:
            messages.error(request, "Account not created! Try again later")
        context = {"form": TeacherRegisterForm()}
        return render(request, "teacher/register.html", context)
