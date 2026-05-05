from rest_framework.permissions import BasePermission


# 🔐 Admin = project creator
class IsProjectAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.created_by == request.user


# 🔐 Member = assigned user
class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user


# 🔐 Only project admin can create task
class CanCreateTask(BasePermission):
    def has_permission(self, request, view):
        project_id = request.data.get("project")

        if not project_id:
            return False

        from workspace.models import Project

        try:
            project = Project.objects.get(id=project_id)
            return project.created_by == request.user
        except Project.DoesNotExist:
            return False



    
from rest_framework.permissions import BasePermission

class CanDeleteTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.created_by == request.user  # 🔥 ONLY ADMIN