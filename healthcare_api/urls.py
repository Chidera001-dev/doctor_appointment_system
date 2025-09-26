# healthcare_api/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UsersAPIView
from .views import DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView ,AppointmentListView, AppointmentDetailView 
#from .views import UserViewSet, DoctorViewSet, AppointmentViewSet
from .register import RegisterView
#from .auth_views import LoginView, LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
#router.register(r'users', UserViewSet, basename='user')
#router.register(r'doctors', DoctorViewSet, basename='doctor')
#router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    #path("login/", LoginView.as_view(), name="login"),
    #path("logout/", LogoutView.as_view(), name="logout"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("admin/users/", UsersAPIView.as_view()),          # GET (list) and POST (create)
    path("admin/users/<int:pk>/", UsersAPIView.as_view()), # PUT (update) and DELETE (remove)


    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
    path("doctors/create/", DoctorCreateView.as_view(), name="doctor-create"),
    path("doctors/<int:pk>/update/", DoctorUpdateView.as_view(), name="doctor-update"),

    path("appointments/", AppointmentListView.as_view(), name="appointment-list"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),


]
urlpatterns += router.urls
