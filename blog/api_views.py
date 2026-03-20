import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Post
from comments.models import Comment
from comments.forms import CommentForm


def serialize_datetime(dt):
    if dt is None:
        return None
    return dt.isoformat()


def post_list_serializer(post):
    return {
        'id': post.id,
        'title': post.title,
        'excerpt': post.excerpt,
        'category_name': post.category.name if post.category else None,
        'tags': [tag.name for tag in post.tags.all()],
        'author_name': post.author.username if post.author else None,
        'created_time': serialize_datetime(post.created_time),
        'views': post.views,
    }


def post_detail_serializer(post):
    try:
        body_html = post.body_html
        toc = post.toc
    except Exception:
        body_html = ''
        toc = ''

    return {
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'body_html': body_html,
        'excerpt': post.excerpt,
        'category_name': post.category.name if post.category else None,
        'tags': [tag.name for tag in post.tags.all()],
        'author_name': post.author.username if post.author else None,
        'created_time': serialize_datetime(post.created_time),
        'modified_time': serialize_datetime(post.modified_time),
        'views': post.views,
        'toc': toc,
    }


def comment_serializer(comment):
    return {
        'id': comment.id,
        'name': comment.name,
        'text': comment.text,
        'created_time': serialize_datetime(comment.created_time),
        'url': comment.url,
    }


@require_http_methods(["GET"])
def api_post_list(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
    except (ValueError, TypeError):
        page = 1
        page_size = 10

    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    if page_size > 50:
        page_size = 50

    posts = Post.objects.all().select_related('category', 'author').prefetch_related('tags')
    paginator = Paginator(posts, page_size)
    page_obj = paginator.get_page(page)

    results = [post_list_serializer(post) for post in page_obj]

    return JsonResponse({
        'count': paginator.count,
        'results': results,
    })


@require_http_methods(["GET"])
def api_post_detail(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post is None:
        return JsonResponse({'error': '文章不存在'}, status=404)

    post.increase_views()

    return JsonResponse(post_detail_serializer(post))


@require_http_methods(["GET", "POST"])
@csrf_exempt
def api_comments(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if post is None:
        return JsonResponse({'error': '文章不存在'}, status=404)

    if request.method == 'GET':
        comments = Comment.objects.filter(post=post).order_by('created_time')
        results = [comment_serializer(comment) for comment in comments]
        return JsonResponse({
            'count': len(results),
            'results': results,
        })

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'errors': {'non_field_errors': ['无效的 JSON 数据']}}, status=400)

        form = CommentForm(data)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return JsonResponse(comment_serializer(comment), status=201)
        else:
            errors = {field: list(messages) for field, messages in form.errors.items()}
            return JsonResponse({'errors': errors}, status=400)
