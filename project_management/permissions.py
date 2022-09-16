from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributor


class IsContributor(BasePermission):
    """
    Object-level permission to only allow contributors to access the projects.
    If the contributor permission is reader then he only can get the information.
    If the contributor permission is editor then he can modify the information.
    """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk') if 'project_pk' in view.kwargs else \
            view.kwargs.get('pk')
        queryset = Contributor.objects.filter(project=project_id, user=request.user)
        if queryset.filter(permission="editor"):
            return True
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        elif queryset.filter(permission="reader") \
                and request.method in SAFE_METHODS:
            return True
        return False
