from django.shortcuts import render
from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework import status


# ✅ Custom permission class for admin checks
class IsAdmin(BasePermission):
    """Only admin users can access this endpoint"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "Admin"


# 🔹 API: Register user (POST) - Public endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# 🔹 HTML: Login page
def login_page(request):
    return render(request, 'login.html')


# 🔹 HTML: Register page
def register_page(request):
    return render(request, 'register.html')


# 🔹 HTML: Dashboard page
def dashboard_page(request):
    return render(request, 'dashboard.html')


# ✅ API: Get authenticated user info
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "role": request.user.role
        }, status=status.HTTP_200_OK)


def admin_dashboard_page(request):
    return render(request, 'admin_dashboard.html')


# ✅ API: Get all users (Admin only)
class AllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """List all users - Admin only"""
        users = User.objects.all().values('id', 'username', 'email', 'first_name', 'role')
        
        return Response({
            "count": users.count(),
            "results": list(users)
        }, status=status.HTTP_200_OK)