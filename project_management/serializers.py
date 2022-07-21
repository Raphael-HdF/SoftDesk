from rest_framework.serializers import ModelSerializer

from project_management.models import Project, Contributor, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'time_created', 'time_updated')


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user_id', 'project_id', 'permission', 'role',)


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id',
                  'time_created',
                  'time_updated')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author_user_id', 'issue_id', 'description', 'time_created',
                  'time_updated')
