from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from .models import Task
from .serializers import TaskSerializer
from .permissions import CanCreateTask, CanDeleteTask, IsTaskOwner


# ✅ CREATE TASK (Only Project Admin)
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateTask]


# ✅ LIST TASKS (Only assigned tasks)
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


# ✅ UPDATE TASK (Admin OR Assigned User)
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        task = self.get_object()

        # 🔐 Admin OR assigned user
        if not (
            task.project.created_by == self.request.user or
            task.assigned_to == self.request.user
        ):
            raise PermissionDenied("Not allowed")

        serializer.save()


# ✅ DELETE TASK (Admin OR Owner)
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, CanDeleteTask]

# ✅ DASHBOARD
class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user)

        return Response({
            "total_tasks": tasks.count(),
            "todo": tasks.filter(status="To Do").count(),
            "in_progress": tasks.filter(status="In Progress").count(),
            "done": tasks.filter(status="Done").count(),
            "overdue": tasks.filter(
                due_date__lt=timezone.now()
            ).exclude(status="Done").count()
        })


# ✅ PROJECT TASK LIST
class ProjectTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project_id=self.kwargs.get("project_id"),
            assigned_to=self.request.user
        )
    



from users.models import User

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        # 🔐 Only Admin allowed
        if request.user.role != "Admin":
            return Response({"error": "Only admin allowed"}, status=403)

        users = User.objects.all()
        data = []

        global_summary = {
            "total_tasks": 0,
            "todo": 0,
            "in_progress": 0,
            "done": 0,
            "overdue": 0
        }

        for user in users:
            tasks = Task.objects.filter(assigned_to=user)

            total = tasks.count()
            done = tasks.filter(status="Done").count()
            progress = tasks.filter(status="In Progress").count()
            todo = tasks.filter(status="To Do").count()
            overdue = tasks.filter(due_date__lt=timezone.now()).exclude(status="Done").count()

            # Add to global summary
            global_summary["total_tasks"] += total
            global_summary["todo"] += todo
            global_summary["in_progress"] += progress
            global_summary["done"] += done
            global_summary["overdue"] += overdue

            # 📊 progress %
            percent = (done / total * 100) if total > 0 else 0

            data.append({
                "username": user.username,
                "name": user.first_name,
                "email": user.email,
                "total_tasks": total,
                "done": done,
                "in_progress": progress,
                "todo": todo,
                "overdue": overdue,
                "progress": round(percent, 2)
            })

        return Response({
            "global_summary": global_summary,
            "users": data
        })
    

class UserTaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):

        if request.user.role != "Admin":
            return Response({"error": "Only admin"}, status=403)

        tasks = Task.objects.filter(assigned_to_id=user_id)

        data = []
        for t in tasks:
            data.append({
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
            })

        return Response(data)