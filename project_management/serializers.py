from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, ValidationError, \
    HyperlinkedModelSerializer, StringRelatedField
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from user.models import User
from user.serializers import UserListSerializer, UserDetailsSerializer, \
    UserNestedSerializer
from SoftDesk.custom_serializers import DynamicFieldsModelSerializer
from project_management.models import Project, Contributor, Issue, Comment


class ProjectNestedSerializer(HyperlinkedModelSerializer):
    # url = HyperlinkedRelatedField(
    #     view_name="project-detail"
    # )
    class Meta:
        model = Project
        fields = "__all__"
        # fields = ('url', 'id', 'title', 'description', 'type', 'time_created',
        #           'time_updated',)

    # def get_queryset(self):


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class IssueSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'project_pk': 'project_id',
    }

    # author_user = UserNestedSerializer(
    #     many=False,
    #     read_only=True,
    # )
    project = ProjectNestedSerializer(many=False, read_only=True)
    author_user = UserListSerializer()
    assignee_user = UserListSerializer()
    # assignee_user = UserNestedSerializer(many=False, read_only=True)

    class Meta:
        model = Issue
        fields = ('url', 'id', 'title', 'description', 'tag', 'priority', 'status',
                  'author_user', 'assignee_user', 'project')
        # extra_kwargs = {'author_user': {'write_only': True}}

    def validate_assignee_user(self, assignee_user):
        """
        Checks if the assignee is registered as a project contributor
        """
        if not Contributor.objects.filter(
                user=assignee_user, project=self.context['project']).exists():
            error_message = f'The assignee {str(assignee_user)} is not' \
                            f' registered as user in the project.'
            raise ValidationError(error_message)
        return assignee_user
