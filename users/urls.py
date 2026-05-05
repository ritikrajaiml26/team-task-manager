from django.urls import path
from .views import (
    RegisterView, login_page, register_page,
    dashboard_page, UserInfoView,
    admin_dashboard_page, AllUsersView
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # 🔹 API endpoints
    path('signup/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('me/', UserInfoView.as_view()),
    path('all-users/', AllUsersView.as_view()),   # ✅ ADD THIS

    # 🔹 HTML pages
    path('login-page/', login_page),
    path('register-page/', register_page),
    path('dashboard-page/', dashboard_page),
    path('admin-dashboard-page/', admin_dashboard_page),
]