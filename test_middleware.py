"""测试 API 接口"""
import json
from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 测试中间件是否正确加载
from blog.middleware import ApiCsrfExemptMiddleware

def test_view(request):
    return JsonResponse({'test': 'ok'})

# 创建一个模拟请求
factory = RequestFactory()

# 测试 GET 请求
request = factory.get('/api/test/')
middleware = ApiCsrfExemptMiddleware()
middleware.process_request(request)
print(f"GET 请求 - _dont_enforce_csrf_checks: {getattr(request, '_dont_enforce_csrf_checks', 'NOT SET')}")

# 测试 POST 请求
request = factory.post('/api/test/', 
                       data=json.dumps({'name': 'test'}),
                       content_type='application/json')
middleware.process_request(request)
print(f"POST 请求 - _dont_enforce_csrf_checks: {getattr(request, '_dont_enforce_csrf_checks', 'NOT SET')}")

# 测试非 API 路径
request = factory.post('/test/')
middleware.process_request(request)
print(f"非 API POST - _dont_enforce_csrf_checks: {getattr(request, '_dont_enforce_csrf_checks', 'NOT SET')}")

print("\n中间件测试完成!")
