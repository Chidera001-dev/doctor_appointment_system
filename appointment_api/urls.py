from django.urls import path

from .views import (
    AppointmentDetailView,
    AppointmentListView,
    AppointmentStatusUpdateView,
    DoctorCreateView,
    DoctorDeleteView,
    DoctorDetailView,
    DoctorListView,
    DoctorUpdateView,
    UserDetailView,
    UserListCreateView,
)

urlpatterns = [
    # Admin - User Management
    path(
        "admin/users/", UserListCreateView.as_view(), name="user-list-create"
    ),  # GET (list) and POST (create)
    path(
        "admin/users/<str:pk>/", UserDetailView.as_view(), name="user-detail"
    ),  # GET, PUT, DELETE
    # Doctors (class-based views)
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),  # List all doctors
    path(
        "doctors/create/", DoctorCreateView.as_view(), name="doctor-create"
    ),  # Create a new doctor
    path(
        "doctors/<str:pk>/", DoctorDetailView.as_view(), name="doctor-detail"
    ),  # Retrieve a doctor by UUID
    path(
        "doctors/<str:pk>/update/", DoctorUpdateView.as_view(), name="doctor-update"
    ),  # Update a doctor by UUID
    path(
        "doctors/<str:pk>/delete/", DoctorDeleteView.as_view(), name="doctor-delete"
    ),  # Delete a doctor by UUID
    # Appointments
    path("appointments/", AppointmentListView.as_view(), name="appointment-list"),
    path(
        "appointments/<str:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    # Appointment Status Update
    path(
        "appointments/<str:pk>/status/",
        AppointmentStatusUpdateView.as_view(),
        name="appointment-status-update",
    ),
]
