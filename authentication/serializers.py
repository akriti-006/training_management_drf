from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


# class RegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'id': {'read_only': True}
#         }

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
#         return data

#     def create(self, validated_data):
#         validated_data.pop('confirm_password')
#         return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")
        self.user = user
        return data

    def to_representation(self, instance):
        user = getattr(self, 'user', None)
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        return {}
    
