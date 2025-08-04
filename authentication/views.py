from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import LoginSerializer, UserSerializer, ResetPasswordSerializer
from training_management.utility.email_functionality import send_welcome_email, send_enquiry_email
from .models import User


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.user
                token, created = Token.objects.get_or_create(user=user)

                # Add group names manually
                group_names = list(user.groups.values_list('name', flat=True))

                return Response({
                    "message": "Login successful",
                    "data": {
                        'email': user.email,
                        'groups': group_names,
                        "token": token.key
                    },
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

            return Response({
                "message": "Login failed",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Login error",
                "data": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({
                "message": "Logout successful",
                "data": None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Logout error",
                "data": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserListView(APIView):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self, request):
        groups = request.query_params.get('groups')
        
        if groups:
            obj = self.model.objects.filter(is_deleted=False, groups=groups)
        else:
            obj = []
        return obj

    def get(self, request):
        try:
            users = self.get_queryset(request)
            serializer = self.serializer_class(users, many=True)
            return Response({
                "message": "User fetched successfully",
                "data": serializer.data}, 
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserDetailView(APIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        
    def get( self, request,pk):
        try:
            obj = self.get_object(pk)
            if not obj:
                return Response({
                    "message": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(obj)
            return Response({
                "message": "User fetched successfully", 
                "data": serializer.data},
                status= status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "data": None},
                            status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not obj:
                return Response({"error": "User not found"}, 
                                status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message":"User updated successfully",
                    "data": serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e), "data": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not obj:
                return Response({"error": "User not found"},
                                status=status.HTTP_404_NOT_FOUND)
            obj.delete()
            return Response({
                "message": "User deleted successfully"},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
