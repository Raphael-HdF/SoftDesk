from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
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
                and request.method in permissions.SAFE_METHODS:
            return True
        return False


class ProjectUsersViewset(ModelViewSet):
    permission_classes = (IsContributor,)
    serializer_class = ContributorListSerializer
    user_serializer_class = UserListSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')

        # if the method is get then display the UserListSerializer and User model
        if self.action in ['retrieve', 'list']:
            return User.objects.filter(contributions__project_id=project_id)

        queryset = Contributor.objects.filter(project=project_id)
        user_id = self.kwargs.get('pk')
        if user_id:
            queryset.filter(user_id=user_id)
        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return self.user_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        # request.POST['user_id'] = int(request.POST.get('user_id'))
        # request.POST['project_id'] = int(
        #     request.POST.get('project_id', 0)
        #     or kwargs.get('project_pk', 0)
        # )
        return super().create(request, *args, **kwargs)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectViewset(ModelViewSet):
    permission_classes = (IsContributor,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(
            contributors__user=self.request.user).distinct()
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
