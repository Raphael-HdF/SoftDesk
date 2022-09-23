from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserListSerializer, UserDetailsSerializer
from user.models import User
from .models import Project, Contributor, Issue, Comment
from .permissions import IsContributor
from .serializers import ProjectCreateSerializer, ProjectSerializer, IssueSerializer


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    # permission_classes = [IsContributor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))
        self.check_object_permissions(request, project)
        # request.data._mutable = True
        # request.data['project'] = project
        # request.data._mutable = False
        serializer = IssueSerializer(
            data=request.data,
            context={
                'request': request,
                'project': kwargs.get('project_pk'),
            }
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                author_user=self.request.user,
                project=Project.objects.get(pk=kwargs.get('project_pk')),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsContributor]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(contributors__user=self.request.user).distinct()
