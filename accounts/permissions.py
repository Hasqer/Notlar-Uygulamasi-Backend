from rest_framework import permissions


class UserGetDataPermission(permissions.BasePermission):
    """Is the owner of the data"""

    def has_object_permission(self, request, view, obj):
        return bool(obj.id == request.user.id)


class IsOwnerPermission(permissions.BasePermission):
    """Is the owner of the object"""

    def has_object_permission(self, request, view, obj):
        return bool(obj.user.id == request.user.id)


class IsSuperUser(permissions.BasePermission):
    """Is the SuperUser"""

    def has_permission(self, request, view):
        return bool(request.user.user_permission == 'superuser')


class IsManager(permissions.BasePermission):
    """Is the Manager"""

    def has_permission(self, request, view):
        return bool(request.user.user_permission in ['manager', 'superuser'])


class IsApiUser(permissions.BasePermission):
    """Is the API User"""

    def has_permission(self, request, view):
        return bool(request.user.user_permission in ['api_user', 'superuser'])


class IsMember(permissions.BasePermission):
    """Is the Member"""

    def has_permission(self, request, view):
        return bool(request.user.user_permission in ['member', 'superuser'])
