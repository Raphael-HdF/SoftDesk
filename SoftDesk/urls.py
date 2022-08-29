"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from rest_framework_nested import routers

from project_management.views import ProjectViewset, ContributorViewset, IssueViewset, \
    CommentViewset, ProjectUsersViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
router.register('contributors', ContributorViewset, basename='contributors')
router.register('issues', IssueViewset, basename='issues')
router.register('comments', CommentViewset, basename='comments')
# router.register(r'projects/(?P<project_id>[^/.]+)/users',
#                 ProjectUsersViewset,
#                 basename='projects-users')

domains_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
domains_router.register('users', ProjectUsersViewset, basename='projects-users')

url_api = 'api-v1/'

urlpatterns = [
    path('admin/', admin.site.urls),

    path(url_api, include(router.urls)),
    path(url_api, include(domains_router.urls)),

    path(url_api, include('user.urls', namespace='user')),
    path(url_api + 'login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(url_api + 'login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
