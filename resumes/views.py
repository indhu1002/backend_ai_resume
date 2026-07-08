from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

        try:
            title = request.data.get("title")
            pdf_file = request.FILES.get("pdf_file")
            user_id = request.data.get("user_id")

            # Validate title

            if not title:
                return Response(
                    {
                        "error": "Resume title is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate PDF file

            if not pdf_file:
                return Response(
                    {
                        "error": "Please select a PDF file"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate user

            if not user_id:
                return Response(
                    {
                        "error": "User ID is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate file type

            if not pdf_file.name.lower().endswith(".pdf"):
                return Response(
                    {
                        "error": "Only PDF files are allowed"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create resume

            resume = Resume.objects.create(
                user_id=user_id,
                title=title,
                pdf_file=pdf_file
            )

            # Extract PDF text

            extracted_text = extract_text_from_pdf(
                resume.pdf_file.path
            )

            # Save extracted text

            resume.extracted_text = extracted_text

            resume.save()

            return Response(
                {
                    "message": "Resume uploaded successfully",

                    "resume_id": resume.id,

                    "resume": {
                        "id": resume.id,
                        "title": resume.title,
                        "text": resume.extracted_text,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            print("RESUME UPLOAD ERROR:", str(e))

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
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
        
        
# class AnalyzeResumeView(APIView):

#     def post(
#         self,
#         request,
#         resume_id
#     ):

#         resume = Resume.objects.get(
#             id=resume_id
#         )

#         result = analyze_resume(
#             resume.extracted_text
#         )

#         analysis = ResumeAnalysis.objects.create(

#             resume=resume,

#             score=result["score"],

#             skills=result["skills"],

#             strengths=result["strengths"],

#             weaknesses=result["weaknesses"],

#             suggestions=result["suggestions"]
#         )

#         return Response({
#             "message":
#             "Analysis Complete"
#         })


class AnalyzeResumeView(APIView):

    def post(self, request, resume_id):

        try:

            resume = Resume.objects.get(
                id=resume_id
            )

            if not resume.extracted_text:

                return Response(
                    {
                        "error":
                        "Resume does not contain extracted text"
                    },
                    status=400
                )

            result = analyze_resume(
                resume.extracted_text
            )

            analysis, created = (
                ResumeAnalysis.objects.update_or_create(

                    resume=resume,

                    defaults={
                        "score":
                        result["score"],

                        "skills":
                        result["skills"],

                        "strengths":
                        result["strengths"],

                        "weaknesses":
                        result["weaknesses"],

                        "suggestions":
                        result["suggestions"],
                    }
                )
            )

            return Response(
                {
                    "message":
                    "Analysis completed successfully",

                    "analysis": {
                        "id":
                        analysis.id,

                        "score":
                        analysis.score,

                        "skills":
                        analysis.skills,

                        "strengths":
                        analysis.strengths,

                        "weaknesses":
                        analysis.weaknesses,

                        "suggestions":
                        analysis.suggestions,
                    }
                },
                status=200
            )

        except Resume.DoesNotExist:

            return Response(
                {
                    "error":
                    "Resume not found"
                },
                status=404
            )

        except Exception as e:

            print(
                "ANALYSIS ERROR:",
                str(e)
            )

            return Response(
                {
                    "error":
                    str(e)
                },
                status=500
            )