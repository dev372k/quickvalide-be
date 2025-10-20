from ..feedback import services
from ..user.models import Profile
from commons.utils.jsonUtil import success_response, error_response
import time
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import ApiLog


def get_user_from_request(request):
    user_id = request.user_id

    if not user_id:
        return None
    return Profile.objects.filter(id=user_id).first()


def create_api_log(request, name, response, duration, message="OK"):
    """
    Generic function to create an API log entry.
    """
    
    ApiLog.objects.create(
        user=get_user_from_request(request),
        name=name,
        end_point=request.path,
        method=request.method,
        status_code=getattr(response, 'status_code', 200),
        message=message,
        response_time=duration
    )


def create_feedback_service(request):
    start_time = time.time()

    res = services.create_feedback_service(request)

    duration = time.time() - start_time

    create_api_log(
        request=request,
        name='create_feedback_service',
        response=res,
        duration=duration,
        message='Feedback created successfully'
    )

    return res


def list_feedback_by_form_service(request, form_uuid):
    start_time = time.time()
    print("hello")
    res = services.list_feedback_by_form_service(request, form_uuid)

    duration = time.time() - start_time

    create_api_log(
        request=request,
        name='list_feedback_by_form_service',
        response=res,
        duration=duration,
        message='Feedback list fetched successfully'
    )

    return res

def delete_feedback_service(request, form_uuid):
    start_time = time.time()

    res = services.delete_feedback_service(request, form_uuid)

    duration = time.time() - start_time

    create_api_log(
        request=request,
        name='delete_feedback_service',
        response=res,
        duration=duration,
        message='Feedback list fetched successfully'
    )

    return res


# API Logs work
def api_call_count_per_day(request):
    api_counts = (
        ApiLog.objects
        .annotate(date=TruncDate('created_at'))  # assuming BaseModel has created_at
        .values('date')
        .annotate(count=Count('id'))
        .order_by('-date')
    )

    return success_response(list(api_counts))

def list_apilogs_by_user_service(request):
    try:
        user = get_user_from_request(request)

        apilogs = (
            ApiLog.objects.filter(user=user)
            .values(
                "id",
                "name",
                "end_point",
                "method",
                "status_code",
                "message",
                "response_time",
                "created_at",
            )
            .order_by("-created_at")
        )

        return success_response(
            data=list(apilogs),
            message="API logs retrieved successfully."
        )

    except Exception as e:
        return error_response(message=str(e), status=500)