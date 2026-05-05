from django.shortcuts import render
from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# 🔹 API: Register user (POST)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# 🔹 HTML: Login page
def login_page(request):
    return render(request, 'login.html')


# 🔹 HTML: Register page
def register_page(request):
    return render(request, 'register.html')


# 🔹 HTML: Dashboard page
def dashboard_page(request):
    return render(request, 'dashboard.html')



class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "first_name": request.user.first_name,
            "role": request.user.role
        })

def admin_dashboard_page(request):
    return render(request, 'admin_dashboard.html')


class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Admin":
            return Response({"error": "Only admin"}, status=403)

        users = User.objects.all()

        data = []
        for u in users:
            data.append({
                "id": u.id,
                "name": u.first_name,
                "username": u.username,
                "email": u.email,
                "role": u.role
            })

        return Response(data)