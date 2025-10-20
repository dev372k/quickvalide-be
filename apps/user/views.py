from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from commons.utils.authUtil import jwt_required
from . import services

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    return services.login_user_service(request)

@csrf_exempt
@jwt_required
@require_http_methods(["GET"])
def get(request):
    return services.get_user_service(request)

@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    return services.create_user_service(request)

@jwt_required
@csrf_exempt
@require_http_methods(["PUT"])
def change_password(request):
    return services.change_user_password(request)

@jwt_required
@csrf_exempt
@require_http_methods(["PUT"])
def update(request):
    return services.update_user(request)

@jwt_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_key(request):
    return services.update_user_api_key(request)

@jwt_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete(request,user_id):
    return services.delete_user(request,user_id)

@jwt_required
@csrf_exempt
@require_http_methods(["PUT"])
def restore(request,user_id):
    return services.restore_user(request,user_id)