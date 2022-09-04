from rest_framework.serializers import ModelSerializer, ValidationError

from SoftDesk.custom_serializers import DynamicFieldsModelSerializer
from project_management.models import Project, Contributor, Issue, Comment


class ContributorListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contributor
        fields = ('user_id', 'project_id', 'permission', 'role',)

    def validate_project_id(self, value):
        # if Contributor.objects.filter(name=value).exists():
        #     raise serializers.ValidationError('Category already exists')
        return value

    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data.get('test'):
            # Levons une ValidationError si ça n'est pas le cas
            raise ValidationError('Name must be in description')
        return data

    # @property
    # def validated_data(self):
    #     test = 'test'
    #     # if not hasattr(self, '_validated_data'):
    #     #     msg = 'You must call `.is_valid()` before accessing `.validated_data`.'
    #     #     raise AssertionError(msg)
    #     return super().validated_data()

    def project_validated_data(self, value):
        return value


class ContributorDetailsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user_id', 'project_id', 'permission', 'role',)


class ProjectSerializer(ModelSerializer):
    contributors = ContributorListSerializer(
        many=True,
        required=False,
        fields=['user_id', 'permission', 'role']
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
