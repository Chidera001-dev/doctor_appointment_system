# from django.contrib.auth import authenticate, login, logout
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import get_user_model

# User = get_user_model()

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .serializers import CustomTokenObtainPairSerializer

# # Login with email + password → returns JWT tokens
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return Response(
#                 {"message": "Login successful"},
#                 status=status.HTTP_200_OK
#             )
#         return Response(
#             {"error": "Invalid credentials"},
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class LogoutView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response(
#             {"message": "Logged out successfully"},
#             status=status.HTTP_200_OK
#         )
