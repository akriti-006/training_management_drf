def has_permission(user, obj):
    return obj.created_by == user or user.is_authenticated
