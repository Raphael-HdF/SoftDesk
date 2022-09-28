from rest_framework.serializers import ModelSerializer, ValidationError
from project_management.models import Project, Contributor, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        try:
            project = Project(**validated_data)
            project.save()
            contributor = Contributor(**{
                "project": project,
                "user": self.context['request'].user,
                "permission": "editor",
                "role": "Author",
            })
            contributor.save()
        except Exception as e:
            raise ValidationError(e)
        return project


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ['project', 'author_user']

    def create(self, validated_data):
        try:
            issue = Issue(**validated_data)
            issue.project_id = self.context["view"].kwargs.get('project_pk')
            issue.author_user = self.context['request'].user
            issue.save()
        except Exception as e:
            raise ValidationError(e)
        return issue

    def validate_assignee_user(self, assignee_user):
        """
        Checks if the assignee is registered as a project contributor
        """
        if not assignee_user.is_superuser:
            contributor = Contributor.objects.filter(
                user=assignee_user,
                project_id=self.context["view"].kwargs.get('project_pk')
            ).exists()
            if not contributor:
                error_message = f'The assignee {str(assignee_user)} is not' \
                                f' registered as contributor in the project.'
                raise ValidationError(error_message)
        return assignee_user


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['issue', 'author_user']

    def create(self, validated_data):
        try:
            comment = Comment(**validated_data)
            comment.issue_id = self.context["view"].kwargs.get('issue_pk')
            comment.author_user = self.context['request'].user
            comment.save()
        except Exception as e:
            raise ValidationError(e)
        return comment


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"
        read_only_fields = ['project']

    def create(self, validated_data):
        try:
            contributor = Contributor(**validated_data)
            contributor.project_id = self.context["view"].kwargs.get('project_pk')
            contributor.save()
        except Exception as e:
            raise ValidationError(e)
        return contributor
