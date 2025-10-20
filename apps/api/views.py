from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import services
from commons.utils.authUtil import jwt_required,api_key_required

# Create your views here.
@csrf_exempt
@api_key_required
@require_http_methods(["POST"])
def create_feedback(request):
    return services.create_feedback_service(request)


@csrf_exempt
@api_key_required
@require_http_methods(["GET"])
def list_feedback_by_form(request, form_uuid):
    return services.list_feedback_by_form_service(request, form_uuid)

@csrf_exempt
@api_key_required
@require_http_methods(["DELETE"])
def delete_feedback(request, feedback_id):
    return services.delete_feedback_service(request, feedback_id)



# API Logs work
@csrf_exempt
@jwt_required
@require_http_methods(["GET"])
def api_call_count_per_day(request):
        return services.api_call_count_per_day(request)

@csrf_exempt
@jwt_required
@require_http_methods(["GET"])
def list_apilogs_by_user_service(request):
        return services.list_apilogs_by_user_service(request)