import json
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from comments.forms import CommentForm


def serialize_post_list(post):
    """序列化文章列表数据"""
    return {
        'id': post.pk,
        'title': post.title,
        'excerpt': post.excerpt,
        'category_name': post.category.name,
        'tags': [tag.name for tag in post.tags.all()],
        'author_name': post.author.username,
        'created_time': post.created_time.isoformat(),
        'views': post.views,
    }


def serialize_post_detail(post):
    """序列化文章详情数据"""
    return {
        'id': post.pk,
        'title': post.title,
        'body': post.body,
        'body_html': post.body_html,
        'excerpt': post.excerpt,
        'category_name': post.category.name,
        'tags': [tag.name for tag in post.tags.all()],
        'author_name': post.author.username,
        'created_time': post.created_time.isoformat(),
        'modified_time': post.modified_time.isoformat(),
        'views': post.views,
        'toc': post.toc,
    }


def serialize_comment(comment):
    """序列化评论数据"""
    return {
        'id': comment.pk,
        'name': comment.name,
        'text': comment.text,
        'created_time': comment.created_time.isoformat(),
        'url': comment.url or '',
    }


@require_http_methods(['GET'])
def post_list(request):
    """获取文章列表接口"""
    posts = Post.objects.all().order_by('-created_time')
    
    # 分页参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    # 限制 page_size 最大为 50
    page_size = min(page_size, 50)
    
    paginator = Paginator(posts, page_size)
    
    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        return JsonResponse({
            'count': paginator.count,
            'results': [],
        })
    
    results = [serialize_post_list(post) for post in page_obj.object_list]
    
    return JsonResponse({
        'count': paginator.count,
        'results': results,
    })


@require_http_methods(['GET'])
def post_detail(request, pk):
    """获取文章详情接口"""
    post = get_object_or_404(Post, pk=pk)
    
    # 阅读量 +1，使用 update 避免触发 Elasticsearch 信号
    Post.objects.filter(pk=pk).update(views=models.F('views') + 1)
    # 重新获取对象以获取最新的 views 值
    post = get_object_or_404(Post, pk=pk)
    
    return JsonResponse(serialize_post_detail(post))


@csrf_exempt
def comments(request, post_pk):
    """获取评论列表或创建评论"""
    # 先检查文章是否存在
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'GET':
        # 按 created_time 正序排列
        comments = post.comment_set.all().order_by('created_time')
        
        results = [serialize_comment(comment) for comment in comments]
        
        return JsonResponse({
            'count': comments.count(),
            'results': results,
        })
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({
                'errors': {
                    'non_field_errors': ['无效的 JSON 格式'],
                }
            }), content_type='application/json')
        
        # 使用 CommentForm 校验数据
        form = CommentForm(data=data)
        
        if form.is_valid():
            # 创建评论但不保存到数据库
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            
            return JsonResponse(serialize_comment(comment), status=201)
        else:
            # 格式化错误信息
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            
            return HttpResponseBadRequest(json.dumps({
                'errors': errors,
            }), content_type='application/json')
    else:
        return HttpResponseBadRequest(json.dumps({
            'errors': {
                'non_field_errors': ['不支持的请求方法'],
            }
        }), content_type='application/json')
