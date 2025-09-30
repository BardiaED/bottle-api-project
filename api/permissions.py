from rest_framework.permissions import BasePermission
from .models import Profile

class IsNotBanned(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = Profile.objects.get(user=user)
        
        if profile.is_banned:
            return False
        else:
            return True