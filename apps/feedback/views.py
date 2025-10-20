from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import services
from commons.utils.authUtil import jwt_required

@csrf_exempt
@require_http_methods(["POST"])
def create_feedback(request):
    return services.create_feedback_service(request)

@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def list_feedback_by_user(request, form_uuid):
    return services.list_feedback_by_user_service(request, form_uuid)

@csrf_exempt
@require_http_methods(["GET"])
def list_feedback_by_form(request, form_uuid):
    return services.list_feedback_by_form_service(request, form_uuid)

@csrf_exempt
@require_http_methods(["DELETE"])
@jwt_required
def delete_feedback(request, feedback_id):
    return services.delete_feedback_service(request, feedback_id)

@csrf_exempt
@jwt_required
@require_http_methods(["GET"])
def feedback_count(request, form_uuid):
    return services.feedback_count_service(request, form_uuid)

