from rest_framework.serializers import ModelSerializer

from SoftDesk.custom_serializers import DynamicFieldsModelSerializer
from project_management.models import Project, Contributor, Issue, Comment


class ContributorListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contributor
        fields = ('user_id', 'project_id', 'permission', 'role',)


class ContributorDetailsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user_id', 'project_id', 'permission', 'role',)


class ProjectSerializer(ModelSerializer):
    contributors = ContributorListSerializer(
        many=True,
        required=False,
        fields=['user', 'permission', 'role']
    )

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'contributors',
                  'time_created', 'time_updated')


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
