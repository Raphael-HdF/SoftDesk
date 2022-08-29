from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserListSerializer, UserDetailsSerializer
from user.models import User
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorListSerializer, \
    ContributorDetailsSerializer, \
    IssueSerializer, \
    CommentSerializer


class ProjectUsersViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        queryset = User.objects.filter(contributions__project_id=project_id)
        if self.request.user in queryset:
            return queryset
        return Response(status=status.HTTP_403_FORBIDDEN)


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
