from rest_framework.views import APIView
from rest_framework.response import Response

from .models import  (
    Resume,
    ResumeAnalysis
)

from .services.pdf_parser import (
    extract_text_from_pdf
)

from .services.gemini_service import (
    analyze_resume
)


class UploadResumeView(APIView):

    def post(self, request):

        file = request.FILES.get("pdf_file")

        title = request.data.get("title")

        user_id = request.data.get("user_id")

        resume = Resume.objects.create(
            user_id=user_id,
            title=title,
            pdf_file=file,
            extracted_text=""
        )

        extracted_text = extract_text_from_pdf(
            resume.pdf_file.path
        )

        resume.extracted_text = extracted_text

        resume.save()

        return Response({
            "message": "Uploaded",
            "resume_id": resume.id
        })
        
from .models import Resume

class ResumeDetailView(APIView):

    def get(self, request, resume_id):

        resume = Resume.objects.get(
            id=resume_id
        )

        return Response({

            "id": resume.id,

            "title": resume.title,

            "text": resume.extracted_text

        })
        
        
class AnalyzeResumeView(APIView):

    def post(
        self,
        request,
        resume_id
    ):

        resume = Resume.objects.get(
            id=resume_id
        )

        result = analyze_resume(
            resume.extracted_text
        )

        analysis = ResumeAnalysis.objects.create(

            resume=resume,

            score=result["score"],

            skills=result["skills"],

            strengths=result["strengths"],

            weaknesses=result["weaknesses"],

            suggestions=result["suggestions"]
        )

        return Response({
            "message":
            "Analysis Complete"
        })