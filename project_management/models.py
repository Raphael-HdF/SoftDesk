from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Project(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=255
    )
    description = models.TextField(
        _('Description'),
        max_length=1080,
        blank=True
    )
    type = models.CharField(
        _('Type'),
        max_length=255,
    )
    time_created = models.DateTimeField(
        _('Created time'),
        auto_now_add=True
    )
    time_updated = models.DateTimeField(
        _('Updated time'),
        auto_now=True
    )

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user_id = models.ForeignKey(
        verbose_name=_('User'),
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    project_id = models.ForeignKey(
        verbose_name=_('Project'),
        to=Project,
        on_delete=models.CASCADE,
    )
    permission = models.CharField(
        verbose_name=_('Permission'),
        choices=[('reader', _('Reader')), ('editor', _('Editor')), ],
        max_length=255,
        default='reader',
    )
    role = models.CharField(
        _('Role'),
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return self.user_id + " - " + self.project_id


class Issue(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=255
    )
    description = models.TextField(
        _('Description'),
        max_length=1080,
        blank=True
    )
    tag = models.CharField(
        _('Tag'),
        max_length=255,
        blank=True
    )
    priority = models.PositiveSmallIntegerField(
        _('Priority'),
        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        default=0
    )
    project_id = models.ForeignKey(
        verbose_name=_('Project'),
        to=Project,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name=_('Status'),
        choices=[
            ('to_do', _('To do')),
            ('in_progress', _('In progress')),
            ('done', _('Done')),
        ],
        default='reader',
        max_length=255,
    )
    author_user_id = models.ForeignKey(
        verbose_name=_('Author'),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="author_issue",
    )
    assignee_user_id = models.ForeignKey(
        verbose_name=_('Assignee User'),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="assigned_issue",
    )
    time_created = models.DateTimeField(
        _('Created time'),
        auto_now_add=True
    )
    time_updated = models.DateTimeField(
        _('Updated time'),
        auto_now=True
    )

    def __str__(self):
        return self.project_id + " : " + self.title


class Comment(models.Model):
    author_user_id = models.ForeignKey(
        verbose_name=_('Author'),
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    issue_id = models.ForeignKey(
        verbose_name=_('Issue'),
        to=Issue,
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        _('Description'),
        max_length=1080,
        blank=True
    )
    time_created = models.DateTimeField(
        _('Created time'),
        auto_now_add=True
    )
    time_updated = models.DateTimeField(
        _('Updated time'),
        auto_now=True
    )

    def __str__(self):
        return self.issue_id + " - " + self.author_user_id

