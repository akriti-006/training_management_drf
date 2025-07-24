from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer

# class RegisterAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             serializer = RegisterSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({
#                     "message": "User registered successfully",
#                     "data": serializer.data
#                 }, status=status.HTTP_201_CREATED)
#             return Response({
#                 "message": "Validation failed",
#                 "data": serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({
#                 "message": "Registration error",
#                 "data": str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.user
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    "message": "Login successful",
                    "data": {
                        'user_data': serializer.data,
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
    # permission_classes = [IsAuthenticated]

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
        

