from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Doctor_Appointment_System API",
      default_version='v1',
      description="API documentation for the Doctor Appointment System",
      contact=openapi.Contact(email="Kellytwinzzy@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),               # Django admin
    path("api/", include("appointment_api.urls")),  # all your app endpoints
    path("auth/", include("authentication.urls")),  # authentication endpoints
    path('swagger<format>.json|.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
