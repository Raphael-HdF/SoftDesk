from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import UserViewSet

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet, basename='user')
