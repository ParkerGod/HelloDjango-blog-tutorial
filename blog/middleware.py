from django.utils.deprecation import MiddlewareMixin


class ApiCsrfExemptMiddleware(MiddlewareMixin):
    """
    为 API 接口豁免 CSRF 检查的中间件
    """
    def process_request(self, request):
        # 检查请求路径是否以 /api/ 开头
        if request.path.startswith('/api/'):
            # 豁免 CSRF 检查
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
