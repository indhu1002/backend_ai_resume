from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):

    def post(self, request):

        data = request.data

        User.objects.create(
            name=data['name'],
            email=data['email'],
            password=make_password(data['password'])
        )

        return Response({
            "message": "User Registered"
        })
        
        


# class LoginView(APIView):

#     def post(self, request):

#         email = request.data['email']
#         password = request.data['password']

#         user = User.objects.get(email=email)

#         if not check_password(password, user.password):

#             return Response({
#                 "message":"Invalid Credentials"
#             }, status=400)

#         refresh = RefreshToken()

#         refresh["user_id"] = user.id

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh)
#         })

class LoginView(APIView):

    def post(self, request):

        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email)

        if not check_password(password, user.password):
            return Response({
                "message": "Invalid Credentials"
            }, status=400)

        refresh = RefreshToken()

        refresh["user_id"] = user.id

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,      # ADD THIS
            "name": user.name,
            "email": user.email
        })
        
from django.http import HttpResponse

def indu(request):
    return HttpResponse("Hello Indu! This is a GET request response.")