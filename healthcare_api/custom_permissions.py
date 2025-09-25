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