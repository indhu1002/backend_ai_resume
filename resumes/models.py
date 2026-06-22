from django.db import models
from users.models import User

class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resumes"
    )

    title = models.CharField(
        max_length=200
    )

    pdf_file = models.FileField(
        upload_to="resumes/"
    )

    extracted_text = models.TextField(  blank=True,
        null=True)

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class ResumeAnalysis(models.Model):

    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    skills = models.JSONField()

    strengths = models.TextField()

    weaknesses = models.TextField()

    suggestions = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )