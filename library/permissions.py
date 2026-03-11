from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.member.role == "admin"


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return request.user.member.role == "student"
    

    