from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print('zsdffmk cgbh  qwertyuiopasdfghjklzxcvbnm,sdfghjklsdfghujk')
        return request.user.is_authenticated and (
            request.user == obj.author
        )