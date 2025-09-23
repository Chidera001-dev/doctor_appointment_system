# healthcare_api/urls.py
from django.urls import path
#from rest_framework.routers import DefaultRouter
#from .views import UserViewSet, DoctorViewSet, AppointmentViewSet
from .register import RegisterView
#from .auth_views import LoginView, LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

#router = DefaultRouter()
#router.register(r'users', UserViewSet, basename='user')
#router.register(r'doctors', DoctorViewSet, basename='doctor')
#router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    #path("login/", LoginView.as_view(), name="login"),
    #path("logout/", LogoutView.as_view(), name="logout"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

#urlpatterns += router.urls
