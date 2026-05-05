from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        help_text="Password must be at least 8 characters long"
    )
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        help_text="Username must be 3-150 characters"
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False},
            'first_name': {'max_length': 150}
        }

    def validate_username(self, value):
        """Ensure username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_role(self, value):
        """Validate role is Admin or Member"""
        if value and value not in ['Admin', 'Member']:
            raise serializers.ValidationError("Role must be 'Admin' or 'Member'.")
        return value

    def create(self, validated_data):
        """Create user with role defaulting to Member"""
        if not validated_data.get('role'):
            validated_data['role'] = 'Member'
        return User.objects.create_user(**validated_data)