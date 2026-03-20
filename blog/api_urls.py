from django.urls import path

from . import api_views

app_name = 'blog_api'

urlpatterns = [
    path('posts/', api_views.PostListAPIView.as_view(), name='post_list'),
    path('posts/<int:pk>/', api_views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<int:pk>/comments/', api_views.CommentListAPIView.as_view(), name='comment_list'),
    path('posts/<int:pk>/comments/create/', api_views.CommentCreateAPIView.as_view(), name='comment_create'),
]
