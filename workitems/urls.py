from django.urls import path
from .views import TaskCreateView, TaskListView, TaskUpdateView, DashboardView,TaskDeleteView
from .views import ProjectTaskListView
from .views import AdminDashboardView,UserTaskDetailView

urlpatterns = [
    path('', TaskListView.as_view()),                 # GET /api/tasks/
    path('create/', TaskCreateView.as_view()),        # POST /api/tasks/create/
    path('<int:pk>/', TaskUpdateView.as_view()),      # PATCH /api/tasks/1/
    path('dashboard/', DashboardView.as_view()),      # GET /api/tasks/dashboard/
    path('<int:pk>/delete/', TaskDeleteView.as_view()),
    path('project/<int:pk>/', ProjectTaskListView.as_view()),
    path('project/<int:project_id>/', ProjectTaskListView.as_view()),
    path('admin-dashboard/', AdminDashboardView.as_view()),
    path('user-tasks/<int:user_id>/', UserTaskDetailView.as_view()),


]

