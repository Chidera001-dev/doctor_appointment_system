from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Only Admin users can access"""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrDoctor(permissions.BasePermission):
    """Allow access to Admins or Doctors"""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or hasattr(user, "doctor_profile"))
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True

        return hasattr(obj, "user") and obj.user == user


class IsAppointmentOwnerOrDoctor(permissions.BasePermission):
    """Patient can access their own appointments,
    Doctor can access appointments assigned to them,
    Admins can access all appointments."""

    def has_permission(self, request, view):
        # Allow all authenticated users to make the request (object-level check comes later)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admins always have access
        if user.is_staff:
            return True

        # Patients can access their own appointments
        if obj.patient == user:
            return True

        # Doctors can access appointments assigned to them
        if hasattr(user, "doctor_profile") and obj.doctor == user.doctor_profile:
            return True

        # Default deny
        return False
