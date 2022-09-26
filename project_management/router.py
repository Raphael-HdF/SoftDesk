from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import ProjectViewSet, IssueViewSet, CommentViewSet

base_router = DefaultRouter()
base_router.register(r'projects', ProjectViewSet, basename='project')

projects_router = NestedSimpleRouter(base_router, r'projects', lookup='project')
projects_router.register(
    r'issues', IssueViewSet, basename='issue'
)

issues_router = NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(
    r'comments', CommentViewSet, basename='comment'
)
