import google.generativeai as genai
import json


genai.configure(
    api_key=config("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

def analyze_resume(text):

    prompt = f"""
Analyze this resume.

Return ONLY JSON.

{{
    "score": 0-100,
    "skills": [],
    "strengths": "",
    "weaknesses": "",
    "suggestions": ""
}}

Resume:

{text}
"""

    response = model.generate_content(
        prompt
    )

    return json.loads(
        response.text
    )