# from rest_framework.permissions import BasePermission, SAFE_METHODS

# class IsHRGroupOrReadOnly(BasePermission):
#     """
#     Only allow users in 'HR' group to edit Teacher and Student details.
#     Others can only view.
#     """
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True

#         return (
#             request.user
#             and request.user.is_authenticated
#             and request.user.groups.filter(name='HR').exists()
#         )


from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrHR(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and
            request.user.groups.filter(name__in=['Admin', 'HR']).exists()
        )

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and
            request.user.groups.filter(name='Teacher').exists()
        )

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and
            request.user.groups.filter(name='Student').exists()
        )
