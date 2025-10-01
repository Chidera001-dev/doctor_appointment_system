from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics , status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserSerializer




class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
