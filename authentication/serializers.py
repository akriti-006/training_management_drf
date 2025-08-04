from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Group


class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Remove fields from the API response
        representation.pop('created_at', None)
        representation.pop('updated_at', None)
        representation.pop('is_deleted', None)
        representation.pop('created_by', None)
        representation.pop('password', None)
        representation.pop('last_login', None)
        representation.pop('user_permissions', None)
        
        return representation


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'  # This shows the group name instead of the ID
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'groups']

    def validate(self, data):
        username = data.get('email')  # authenticate() still needs username
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")

        self.user = user
        return data

    
class UserSerializer(BaseSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'  # This shows the group name instead of the ID
    )

    class Meta:
        model = User
        fields = "__all__"


class ResetPasswordSerializer(BaseSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def validate(self, data):
        user = self.context['request'].user

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'old_password': 'Incorrect old password.'})

        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'confirm_new_password': 'Passwords do not match.'})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
