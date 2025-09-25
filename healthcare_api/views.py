from django.shortcuts import render
from .models import DoctorProfile, Appointment
from .serializers import (
    RegisterSerializer, UserSerializer, DoctorProfileSerializer, 
    AppointmentSerializer
)
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser,  IsAdminOrDoctor
from django.contrib.auth import get_user_model
User = get_user_model()


# for user management by admin
class UsersAPIView(APIView):
    permission_classes = [IsAdminUser]  # Only admin can view users
    
    def get(self, request):
        """List all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """Update an existing user"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

    # 🔒 Prevent non-admins from setting is_staff
        if not request.user.is_staff and "is_staff" in data:
            data.pop("is_staff")

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        """Delete a user"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """Admin can view, update, or delete any user"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]

    # def perform_update(self, serializer):
    #     """Admin can set is_doctor and is_staff flags"""
    #     # Only admin can set is_staff (staff can't promote to admin)
    #     if not self.request.user.is_staff:
    #         if 'is_staff' in serializer.validated_data:
    #             del serializer.validated_data['is_staff']
    #     serializer.save()


# for viewsets (DoctorProfileViewSet)  
class DoctorListView(generics.ListAPIView):
    """List all doctors - accessible to all authenticated users"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

class DoctorDetailView(generics.RetrieveAPIView):
    """Retrieve a specific doctor's profile - accessible to all authenticated users"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

class DoctorCreateView(generics.CreateAPIView):
    """Only Admin can create doctor profiles"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAdminUser]

class DoctorUpdateView(generics.UpdateAPIView):
    """Admin can update any doctor, Doctor can update their own profile"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated , IsAdminOrDoctor]

    def get_queryset(self):
        """Doctors can only update their own profile"""
        if self.request.user.is_doctor:
            return DoctorProfile.objects.filter(user=self.request.user)
        return DoctorProfile.objects.all()