from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import ProjectViewSet, IssueViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
projects_router = NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(
    r'issues', IssueViewSet, basename='issue'
)
# router.register(r'budget-groups', BudgetGroupViewSet)
# group_router = NestedSimpleRouter(router, r'budget-groups', lookup='group')
# group_router.register(r'collaborators', CollaboratorsViewSet, basename='collaborator')