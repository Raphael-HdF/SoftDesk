from rest_framework.serializers import ModelSerializer, ValidationError

from SoftDesk.custom_serializers import DynamicFieldsModelSerializer
from project_management.models import Project, Contributor, Issue, Comment


class ContributorListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contributor
        fields = ('user', 'project', 'permission', 'role',)


class ContributorDetailsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'project', 'permission', 'role',)


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
        fields = ('id', 'title', 'description', 'tag', 'priority', 'project',
                  'status', 'author_user', 'assignee_user', 'time_created',
                  'time_updated')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author_user', 'issue', 'description', 'time_created',
                  'time_updated')
