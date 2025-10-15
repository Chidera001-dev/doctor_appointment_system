from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.serializers import UserSerializer

from .models import Appointment, DoctorProfile
from .permissions import IsAdminOrDoctor, IsAdminUser, IsAppointmentOwnerOrDoctor
from .serializers import AppointmentSerializer, DoctorProfileSerializer

User = get_user_model()


# User Management (Admin)


class UserListCreateView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="List all users")
    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Create a new user")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Retrieve a user by UUID")
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Update a user by UUID")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        if not request.user.is_staff and "is_staff" in data:
            data.pop("is_staff")
        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete a user by UUID")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Doctor Views


class DoctorListView(generics.GenericAPIView):
    queryset = DoctorProfile.objects.order_by("pk")
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["specialization", "experience_years"]
    search_fields = ["specialization"]
    ordering_fields = ["experience_years"]
    ordering = ["-experience_years"]
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(operation_summary="List all doctors")
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        #  pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DoctorDetailView(generics.GenericAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        # Fetch DoctorProfile using the user UUID passed in the URL as pk
        user_id = self.kwargs["pk"]
        return get_object_or_404(DoctorProfile, user__id=user_id)

    @swagger_auto_schema(operation_summary="Retrieve a doctor profile by UUID")
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DoctorCreateView(generics.GenericAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Create a new doctor profile")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorUpdateView(generics.GenericAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    def get_object(self):
        # Fetch DoctorProfile by the related user's UUID from URL
        user_id = self.kwargs["pk"]
        return get_object_or_404(DoctorProfile, user__id=user_id)

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor and not user.is_staff:
            return DoctorProfile.objects.filter(user=user)
        return DoctorProfile.objects.all()

    @swagger_auto_schema(operation_summary="Update a doctor profile")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDeleteView(generics.GenericAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        # Fetch DoctorProfile by the related user's UUID from URL
        user_id = self.kwargs["pk"]
        return get_object_or_404(DoctorProfile, user__id=user_id)

    @swagger_auto_schema(operation_summary="Delete a doctor profile (Admin only)")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": f"Doctor profile with ID {instance.id} has been deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


# Appointment Views


class AppointmentListView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrDoctor]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        elif user.is_doctor:
            return Appointment.objects.filter(doctor=user.doctor_profile)
        else:
            return Appointment.objects.filter(patient=user)

    @swagger_auto_schema(operation_summary="List appointments (depends on role)")
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Create a new appointment (Patients only)")
    def post(self, request, *args, **kwargs):
        if request.user.is_doctor or request.user.is_staff:
            return Response(
                {"error": "Only patients can book appointments"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(generics.GenericAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAppointmentOwnerOrDoctor]
    lookup_field = "id"

    def get_object(self):
        # Fetch Appointment by its own PK (or UUID if you change it)
        appointment_id = self.kwargs["pk"]
        return get_object_or_404(Appointment, id=appointment_id)

    @swagger_auto_schema(operation_summary="Retrieve an appointment by UUID")
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Update an appointment by UUID")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete an appointment by UUID")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentStatusUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrDoctor]

    @swagger_auto_schema(operation_summary="Doctor confirms or cancels an appointment")
    def patch(self, request, *args, **kwargs):
        appointment = self.get_object()

        # Only the doctor assigned to this appointment (or admin) can update it
        if not (request.user.is_staff or appointment.doctor.user == request.user):
            return Response(
                {"error": "You are not allowed to modify this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        status_choice = request.data.get("status")
        if status_choice not in ["confirmed", "cancelled"]:
            return Response(
                {"error": "Invalid status. Choose 'confirmed' or 'cancelled'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = status_choice
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
