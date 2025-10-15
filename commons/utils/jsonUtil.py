# myapp/utils/jsonUtil.py
from django.http import JsonResponse

def success_response(data=None, message="Success", status=200):
    """
    Returns a standardized success JSON response.
    """
    return JsonResponse({
        "status": "success",
        "message": message,
        "data": data
    }, status=status, safe=False)


def error_response(message="Something went wrong", status=400, errors=None):
    """
    Returns a standardized error JSON response.
    """
    return JsonResponse({
        "status": "error",
        "message": message,
        "errors": errors
    }, status=status, safe=False)
