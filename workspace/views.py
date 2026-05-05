from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Project
from .serializers import ProjectSerializer
from users.models import User


# ✅ Create Project
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)  # creator auto member


# ✅ List Projects (only where user is member)
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)


# ✅ Add Member (Admin only)
class AddMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        # 🔒 Only creator (admin)
        if project.created_by != request.user:
            return Response(
                {"error": "Only admin can add members"},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)

        project.members.add(user)

        return Response({"message": "Member added successfully"})


# ✅ Remove Member (Admin only)
class RemoveMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        if project.created_by != request.user:
            return Response(
                {"error": "Only admin can remove members"},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)

        project.members.remove(user)

        return Response({"message": "Member removed successfully"})