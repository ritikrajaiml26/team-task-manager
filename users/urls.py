from django.urls import path
from .views import (
    RegisterView, login_page, register_page,
    dashboard_page, UserInfoView,
    admin_dashboard_page, AllUsersView
)

urlpatterns = [
    # 🔹 API endpoints
    path('signup/', RegisterView.as_view()),        # POST /api/users/signup/
    path('me/', UserInfoView.as_view()),             # GET  /api/users/me/
    path('all-users/', AllUsersView.as_view()),      # GET  /api/users/all-users/

    # 🔹 HTML pages
    path('login-page/', login_page),
    path('register-page/', register_page),
    path('dashboard-page/', dashboard_page),
    path('admin-dashboard-page/', admin_dashboard_page),
]