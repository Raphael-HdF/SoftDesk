from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserListSerializer, UserDetailsSerializer
from user.models import User
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorListSerializer, \
    ContributorDetailsSerializer, \
    IssueSerializer, \
    CommentSerializer

class IsContributor(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Instance must have an attribute named `owner`.
        project_id = view.kwargs.get('project_pk')
        queryset = User.objects.filter(contributions__project_id=project_id)
        return request.user in queryset

class ProjectUsersViewset(ModelViewSet):
    permission_classes = (IsContributor,)
    serializer_class = UserListSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        queryset = User.objects.filter(contributions__project_id=project_id)
        # if self.request.user in queryset:
        return queryset
        # return []
        # return Response([{'error': "You don't have the permission to view this project"}],
        #                 status=status.HTTP_403_FORBIDDEN)
        # return


class ProjectViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(
            contributors__user=self.request.user).distinct()
        # project_id = self.request.GET.get('project_id')
        # if project_id:
        #     queryset = queryset.filter(project_id=project_id)
        return queryset


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorListSerializer
    details_serializer_class = ContributorDetailsSerializer

    def get_queryset(self):
        return Contributor.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.details_serializer_class
        return super().get_serializer_class()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()
        # return Issue.objects.filter(
        #     author_user__username__contains="adm").distinct()


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
