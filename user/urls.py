from django.urls import path, include

from .router import users_router
from .views import RegisterUser

app_name = 'user'

urlpatterns = [
    path('signup/', RegisterUser.as_view(), name='register_user'),
    path('', include(users_router.urls)),
]
