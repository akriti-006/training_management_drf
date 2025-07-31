# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHRGroupOrReadOnly(BasePermission):
    """
    Only allow users in 'HR' group to edit Teacher and Student details.
    """

    def has_permission(self, request, view):
        # Allow all users to view (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Only allow editing if user is in HR group
        return request.user.groups.filter(name='HR').exists()
