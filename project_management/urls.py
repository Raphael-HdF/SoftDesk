from django.urls import path, include

from .router import *

urlpatterns = [
    path('', include(base_router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
]
