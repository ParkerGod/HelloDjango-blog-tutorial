from django.urls import path

from blog import api_views

app_name = 'api'

urlpatterns = [
    path('posts/', api_views.post_list, name='post_list'),
    path('posts/<int:pk>/', api_views.post_detail, name='post_detail'),
    path('posts/<int:post_pk>/comments/', api_views.comments, name='comments'),
]
