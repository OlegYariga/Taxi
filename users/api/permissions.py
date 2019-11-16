from rest_framework import permissions


class BaseUserPermission(permissions.BasePermission):
    message = 'need to login'

    def has_permission(self, request, view):
        try:
            return bool(request.user.passenger or request.user.driver)
        except:
            return False

class PassengerPermission(permissions.BasePermission):
    message = 'need login as passenger'

    def has_permission(self, request, view):
        try:
            return bool(request.user.passenger and request.user.is_authenticated)
        except AttributeError:
            return False


class DriverPermission(permissions.BasePermission):
    message = 'need login as driver'

    def has_permission(self, request, view):
        try:
            return bool(request.user.driver and request.user.is_authenticated)
        except AttributeError:
            return False
