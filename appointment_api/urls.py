from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserListCreateView, UserDetailView,   
    DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView,
    AppointmentListView, AppointmentDetailView, DoctorProfileViewSet
)

# Router for ViewSets
router = DefaultRouter()
router.register(r'doctor-profiles', DoctorProfileViewSet, basename='doctor-profile')

urlpatterns = [
    # Admin - User Management
    path("admin/users/", UserListCreateView.as_view(), name="user-list-create"),   # GET (list) and POST (create)
    path("admin/users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),   # GET, PUT, DELETE

    # Doctors (class-based views)
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
    path("doctors/create/", DoctorCreateView.as_view(), name="doctor-create"),
    path("doctors/<int:pk>/update/", DoctorUpdateView.as_view(), name="doctor-update"),

    # Appointments
    path("appointments/", AppointmentListView.as_view(), name="appointment-list"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),

    # Include router URLs for DoctorProfileViewSet
    path("", include(router.urls)),
]

