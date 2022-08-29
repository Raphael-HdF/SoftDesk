from django.contrib import admin

from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdminConfig(admin.ModelAdmin):
    model = Project
    search_fields = ('title', 'description',)
    # list_filter = ('user',)
    ordering = ('-time_created',)
    list_display = ('id', 'title', 'type',)


@admin.register(Contributor)
class ContributorAdminConfig(admin.ModelAdmin):
    model = Contributor
    search_fields = ('user', 'project',)
    list_filter = ('user',)
    # ordering = ('-time_created',)
    list_display = ('user', 'project', 'permission', 'role',)


@admin.register(Issue)
class IssueAdminConfig(admin.ModelAdmin):
    model = Issue
    search_fields = ('title', 'description', 'tag',)
    list_filter = ('project',)
    ordering = ('-time_created',)
    list_display = ('title', 'tag', 'priority', 'project', 'status')


@admin.register(Comment)
class CommentAdminConfig(admin.ModelAdmin):
    model = Comment
    search_fields = ('author_user', 'description', 'issue',)
    list_filter = ('issue', 'author_user')
    ordering = ('-time_created',)
    list_display = ('author_user', 'issue', 'description', 'time_created',)
