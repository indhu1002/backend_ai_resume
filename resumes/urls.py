from django.urls import path
from .views import AnalyzeResumeView, ResumeDetailView, UploadResumeView

urlpatterns = [

    path(
        "upload/",
        UploadResumeView.as_view()
    ),
    path(
    "<int:resume_id>/",
    ResumeDetailView.as_view()
),
    path(
    "<int:resume_id>/analyze/",
    AnalyzeResumeView.as_view()
),
]



