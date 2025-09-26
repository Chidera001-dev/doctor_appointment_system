from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Only Admin users can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# class IsDoctor(permissions.BasePermission):
#     """Only Doctors can access"""
#     def has_permission(self, request, view):
#         return request.user and request.user.is_doctor
    

class IsAdminOrDoctor(permissions.BasePermission):
    """Both Admin and Doctors can access"""
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_doctor)


class IsAppointmentOwnerOrDoctor(permissions.BasePermission):
    """Patient can access their appointments, Doctor can access appointments assigned to them"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        # Patient can access their own appointments
        if obj.patient == request.user:
            return True
        
        # Doctor can access appointments assigned to them
        if hasattr(request.user, 'doctor_profile') and obj.doctor == request.user.doctor_profile:
            return True
        
        return False