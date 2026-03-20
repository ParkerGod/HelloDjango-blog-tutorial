from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import api_views

app_name = 'api'
urlpatterns = [
    path('posts/', api_views.api_post_list, name='post_list'),
    path('posts/<int:pk>/', api_views.api_post_detail, name='post_detail'),
    path('posts/<int:pk>/comments/', csrf_exempt(api_views.api_comments), name='comments'),
]
