from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def api_root(request):
    """API根路径，返回API信息"""
    return JsonResponse({
        'message': '百科系统API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/',
            'auth': '/api/auth/',
            'entries': '/api/entries/',
            'categories': '/api/categories/',
            'favorites': '/api/favorites/',
            'search': '/api/search/'
        }
    })