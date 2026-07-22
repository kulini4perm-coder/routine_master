from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Проверка авторизованного пользователя на владельца привычки """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
