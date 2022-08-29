from django.urls import path

from .views import RegisterUser

app_name = 'user'

urlpatterns = [
    path('signup/', RegisterUser.as_view(), name='register_user'),
]