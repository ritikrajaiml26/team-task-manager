from django.urls import path
from .views import ProjectCreateView, ProjectListView,AddMemberView,RemoveMemberView

urlpatterns = [
    path('create/', ProjectCreateView.as_view()),
    path('list/', ProjectListView.as_view()),
    path('<int:pk>/add-member/', AddMemberView.as_view()),
    path('<int:pk>/remove-member/', RemoveMemberView.as_view()),

]

