from rest_framework.viewsets import ModelViewSet

from .models import Project, Contributor, Issue, Comment
from .permissions import IsContributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, \
    ContributorSerializer


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        return Comment.objects.filter(
            issue_id=self.kwargs['issue_pk'],
        )


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        return Contributor.objects.filter(
            project=self.kwargs['project_pk']
        )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(contributors__user=self.request.user).distinct()
