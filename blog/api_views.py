import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from comments.forms import CommentForm
from .models import Post


def serialize_datetime(dt):
    """将 datetime 转换为 ISO 格式字符串"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


class PostListAPIView(View):
    """GET /api/posts/ - 文章列表"""

    def get(self, request):
        # 获取分页参数
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
        except ValueError:
            return JsonResponse({'error': 'Invalid page or page_size'}, status=400)

        # 限制 page_size 最大为 50
        if page_size > 50:
            page_size = 50
        if page_size < 1:
            page_size = 10
        if page < 1:
            page = 1

        # 获取所有文章，按 created_time 倒序
        all_posts = Post.objects.all().order_by('-created_time')
        total_count = all_posts.count()

        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        posts = all_posts[start:end]

        # 序列化数据
        results = []
        for post in posts:
            results.append({
                'id': post.id,
                'title': post.title,
                'excerpt': post.excerpt,
                'category': post.category.name if post.category else None,
                'tags': [tag.name for tag in post.tags.all()],
                'author': post.author.username if post.author else None,
                'created_time': serialize_datetime(post.created_time),
                'views': post.views,
            })

        return JsonResponse({
            'count': total_count,
            'results': results
        })


class PostDetailAPIView(View):
    """GET /api/posts/<pk>/ - 文章详情"""

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # 阅读量 +1（使用 QuerySet.update 避免触发信号）
        Post.objects.filter(pk=post.pk).update(views=post.views + 1)
        post.views += 1

        data = {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'body_html': post.body_html,
            'excerpt': post.excerpt,
            'category': post.category.name if post.category else None,
            'tags': [tag.name for tag in post.tags.all()],
            'author': post.author.username if post.author else None,
            'created_time': serialize_datetime(post.created_time),
            'modified_time': serialize_datetime(post.modified_time),
            'views': post.views,
            'toc': post.toc,
        }

        return JsonResponse(data)


class CommentListAPIView(View):
    """GET /api/posts/<pk>/comments/ - 评论列表"""

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.all().order_by('created_time')

        results = []
        for comment in comments:
            results.append({
                'id': comment.id,
                'name': comment.name,
                'text': comment.text,
                'created_time': serialize_datetime(comment.created_time),
                'url': comment.url,
            })

        return JsonResponse({'results': results})


@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateAPIView(View):
    """POST /api/posts/<pk>/comments/ - 提交评论"""

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # 解析 JSON 请求体
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'errors': {'__all__': ['Invalid JSON']}}, status=400)

        # 使用 CommentForm 校验数据
        form = CommentForm(data)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            # 设置 is_approved 字段（如果存在）
            if hasattr(comment, 'is_approved'):
                comment.is_approved = True
            comment.save()

            # 返回新评论的 JSON
            response_data = {
                'id': comment.id,
                'name': comment.name,
                'text': comment.text,
                'created_time': serialize_datetime(comment.created_time),
                'url': comment.url,
            }
            return JsonResponse(response_data, status=201)
        else:
            # 格式化错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
            return JsonResponse({'errors': errors}, status=400)
