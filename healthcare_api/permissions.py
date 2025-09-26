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
    
class  IsAppointmentOwnerOrDoctor(permissions.BasePermission):
    """Patients can manage their own appointments, Doctors can manage appointments assigned to them"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True  # Admin can access all appointments
        elif user.is_doctor:
            return obj.doctor.user == user  # Doctors can access appointments assigned to them
        else:
            return obj.patient == user  # Patients can access their own appointments