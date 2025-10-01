from django.contrib.auth import get_user_model
from rest_framework import generics, status, filters,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import DoctorProfile, Appointment
from .serializers import (
    UserSerializer, DoctorProfileSerializer, AppointmentSerializer
)
from .permissions import IsAdminUser, IsAdminOrDoctor, IsAppointmentOwnerOrDoctor

User = get_user_model()


class DoctorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DoctorProfile.
    Admin can manage all, Doctors can manage their own.
    """
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    def get_queryset(self):
        user = self.request.user
        # Doctor sees only their own profile
        if user.is_doctor and not user.is_staff:
            return DoctorProfile.objects.filter(user=user)
        return DoctorProfile.objects.all()

    @swagger_auto_schema(
        operation_description="List all doctor profiles. Doctors see only their own profile.",
        responses={200: DoctorProfileSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a doctor profile by ID",
        responses={200: DoctorProfileSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new doctor profile (Admin only)",
        request_body=DoctorProfileSerializer,
        responses={201: DoctorProfileSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a doctor profile (Admin or the doctor themselves)",
        request_body=DoctorProfileSerializer,
        responses={200: DoctorProfileSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a doctor profile (Admin only)",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------
# User Management (Admin)
# -------------------------
class UserListCreateView(generics.ListCreateAPIView):
    """Admin can list all users or create a new one"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_description="List all users", responses={200: UserSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new user", request_body=UserSerializer, responses={201: UserSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin can view, update, or delete any user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_description="Retrieve a user by ID", responses={200: UserSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a user by ID", request_body=UserSerializer, responses={200: UserSerializer})
    def put(self, request, *args, **kwargs):
        # Prevent non-admin from setting is_staff (extra safeguard)
        if not request.user.is_staff and "is_staff" in request.data:
            data = request.data.copy()
            data.pop("is_staff")
            serializer = self.get_serializer(self.get_object(), data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a user by ID", responses={204: "No Content"})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# -------------------------
# Doctor Views
# -------------------------
class DoctorListView(generics.ListAPIView):
    """List all doctors - accessible to all authenticated users"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'experience_years']
    search_fields = ['specialization']
    ordering_fields = ['experience_years']
    ordering = ['-experience_years']

    @swagger_auto_schema(operation_description="List all doctors", responses={200: DoctorProfileSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DoctorDetailView(generics.RetrieveAPIView):
    """Retrieve a specific doctor's profile - accessible to all authenticated users"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve a doctor profile by ID", responses={200: DoctorProfileSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DoctorCreateView(generics.CreateAPIView):
    """Only Admin can create doctor profiles"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_description="Create a new doctor profile", request_body=DoctorProfileSerializer, responses={201: DoctorProfileSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DoctorUpdateView(generics.UpdateAPIView):
    """Admin can update any doctor, Doctor can update their own profile"""
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    def get_queryset(self):
        if self.request.user.is_doctor:
            return DoctorProfile.objects.filter(user=self.request.user)
        return DoctorProfile.objects.all()

    @swagger_auto_schema(operation_description="Update a doctor profile", request_body=DoctorProfileSerializer, responses={200: DoctorProfileSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


# -------------------------
# Appointment Views
# -------------------------
class AppointmentListView(generics.ListCreateAPIView):
    """Patients can see their appointments, Doctors can see theirs, Admin sees all"""
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

    @swagger_auto_schema(operation_description="List appointments (depends on role)", responses={200: AppointmentSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new appointment (Patients only)", request_body=AppointmentSerializer, responses={201: AppointmentSerializer})
    def post(self, request, *args, **kwargs):
        if request.user.is_doctor or request.user.is_staff:
            return Response(
                {"error": "Only patients can book appointments"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Patients can view/cancel their appointments, Doctors can confirm/reject"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAppointmentOwnerOrDoctor]

    @swagger_auto_schema(operation_description="Retrieve an appointment by ID", responses={200: AppointmentSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an appointment by ID", request_body=AppointmentSerializer, responses={200: AppointmentSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete an appointment by ID", responses={204: "No Content"})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
