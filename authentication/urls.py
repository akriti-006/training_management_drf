from django.urls import path
from .views import LoginAPIView, LogoutAPIView, UserListView, UserDetailView, ResetPasswordView

urlpatterns = [
    # path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
