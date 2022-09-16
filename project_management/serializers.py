from rest_framework.serializers import ModelSerializer, ValidationError, \
    HyperlinkedModelSerializer, StringRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from user.models import User
from user.serializers import UserListSerializer, UserDetailsSerializer
from SoftDesk.custom_serializers import DynamicFieldsModelSerializer
from project_management.models import Project, Contributor, Issue, Comment


class IssueSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'project_pk': 'project_id',
    }
    author_user = UserDetailsSerializer(many=False, read_only=True)
    assignee_user = UserDetailsSerializer(many=False, required=False, read_only=False)

    class Meta:
        model = Issue
        fields = ('url', 'id', 'title', 'description', 'tag', 'priority', 'status',
                  'author_user', 'assignee_user')
        extra_kwargs = {'author_user': {'write_only': True}}

    def validate_assignee_user(self, assignee):
        """
        Checks if the assignee is registered as a project contributor
        """
        user_id = User.objects.get(username=assignee).id
        if not Contributor.objects.filter(
                       user=user_id, project=self.context['project']).exists():
            error_message = 'The assignee '\
                            + str(assignee)\
                            + ' is not registered for the project.'
            raise ValidationError(error_message)
        return assignee


# class CollaboratorSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'first_name', 'last_name', 'email')


class ProjectSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('url', 'id', 'title', 'description', 'type', 'time_created',
                  'time_updated')


class ProjectCreateSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

# class BudgetGroupSerializer(NestedHyperlinkedModelSerializer):
#     budgets = StringRelatedField(many=True, allow_empty=True)
#     collaborators = CollaboratorSerializer(many=True)
#
#     class Meta:
#         model = BudgetGroup
#         fields = ('url', 'name', 'budgets', 'collaborators')
