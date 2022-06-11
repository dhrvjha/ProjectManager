from django.urls import path

from student.views import StudentApplicationStatusView, StudentRequestView

urlpatterns = [
    path("apply/", StudentRequestView.as_view(), name="student_apply"),
    path(
        "status/<int:studentId>/",
        StudentApplicationStatusView.as_view(),
        name="student_status",
    ),
]
