from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == "ADMIN"

class IsSOC(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == "SOC"

class IsInvestigator(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == "INVESTIGATOR"

class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == "VIEWER"


class IsAdminOrSOC(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role in ["ADMIN", "SOC"]



    