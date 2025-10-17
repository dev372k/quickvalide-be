from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import services
from commons.utils.authUtil import jwt_required

# Create Form
@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def create_form(request):
    return services.create_form_service(request)

# List Forms
@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def list_forms(request):
    return services.list_forms_service(request)

# Get Form by UUID
@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def get_form(request, uuid):
    return services.get_form_service(request, uuid)

# Get Form by UUID
@csrf_exempt
@require_http_methods(["GET"])
def get_form_details(request, uuid):
    return services.get_form_details_service(request, uuid)

# Update Form
@csrf_exempt
@require_http_methods(["PUT"])
@jwt_required
def update_form(request, uuid):
    return services.update_form_service(request, uuid)

# Soft Delete Form
@csrf_exempt
@require_http_methods(["DELETE"])
@jwt_required
def delete_form(request, uuid):
    return services.delete_form_service(request, uuid)

# Restore Soft-Deleted Form
@csrf_exempt
@require_http_methods(["PUT"])
@jwt_required
def restore_form(request, uuid):
    return services.restore_form_service(request, uuid)

# Toggle is_public
@csrf_exempt
@require_http_methods(["PUT"])
@jwt_required
def toggle_publish_form(request, uuid):
    return services.toggle_publish_form_service(request, uuid)
