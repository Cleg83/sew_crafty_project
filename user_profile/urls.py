from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('get-profile-info/', views.get_user_profile_info, name='get_profile_info'),
]