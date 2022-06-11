"""
urls for teacher

/ -> home
requests/ -> request from students
projects/ -> projects completed under teacher
register/ -> register new teacher
login/ -> login a teacher
logout/ -> logout a teacher
"""


from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path

from teacher.views import (
    ProjectRequestDetailView,
    ProjectRequestView,
    ProjectsView,
    RegisterTeacher,
    TeacherHomeView,
)

urlpatterns = [
    path("", TeacherHomeView.as_view(), name="teacher_home"),
    path(
        "requests/",
        login_required(ProjectRequestView.as_view()),
        name="project_request_view",
    ),
    path("projects/", login_required(ProjectsView.as_view()), name="projects_view"),
    path(
        "login/",
        views.LoginView.as_view(template_name="teacher/login.html"),
        name="login",
    ),
    path("register/", RegisterTeacher.as_view(), name="register"),
    path(
        "logout/",
        views.LogoutView.as_view(template_name="teacher/logout.html"),
        name="logout",
    ),
    path(
        "requests/detail/<uuid:projectRequestId>/",
        ProjectRequestDetailView.as_view(),
        name="project_request_detail",
    ),
]
