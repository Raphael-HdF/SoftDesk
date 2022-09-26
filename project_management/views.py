from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserListSerializer, UserDetailsSerializer
from user.models import User
from .models import Project, Contributor, Issue, Comment
from .permissions import IsContributor
from .serializers import ProjectSerializer, IssueSerializer


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    # permission_classes = [IsContributor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    # def create(self, request, *args, **kwargs):
    #     return super(IssueViewSet, self).create(request, *args, **kwargs)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    # permission_classes = [IsContributor]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(contributors__user=self.request.user).distinct()
