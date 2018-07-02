from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists() or obj.professor == request.user

class isProfessor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.professor == request.user

# create isParent permission (maybe)