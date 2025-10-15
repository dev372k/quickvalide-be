from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import services

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    return services.login_user_service(request)

@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    return services.create_user_service(request)