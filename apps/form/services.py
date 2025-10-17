import json
from django.utils.text import slugify
from .models import Form
from ..user.models import Profile
from commons.utils.jsonUtil import success_response, error_response


def get_user_from_request(request):
    user_id = request.user_id

    if not user_id:
        return None
    return Profile.objects.filter(id=user_id).first()


def create_form_service(request):
    try:
        user_id = request.user_id
        print("User ID from request:", user_id)
        user = get_user_from_request(request)
        if not user:
            return error_response("User not found", status=401)

        data = json.loads(request.body)
        title = data.get("title")
        if not title:
            return error_response("Title is required", status=400)

        slug = slugify(title)

        form = Form.objects.create(
            user=user,
            title=title,
            description=data.get("description", ""),
            slug=slug,
            redirect_url=data.get("redirect_url"),
            theme=data.get("theme", {}),
            widget_theme=data.get("widget_theme", {}),
            is_public=data.get("is_public", False),
        )

        return success_response(
            message="Form created successfully.",
            data={"uuid": str(form.uuid), "title": form.title,"description" : form.description, "created_at": form.created_at},
        )

    except Exception as e:
        return error_response(message=str(e), status=500)


def list_forms_service(request, include_deleted=False):
    try:
        user = get_user_from_request(request)
        if not user:
            return error_response("User not found", status=401)

        queryset = Form.objects.filter(user=user)
        if not include_deleted:
            queryset = queryset.filter(is_deleted=False)

        forms = queryset.values(
            "uuid", "title", "description", "slug", "is_public", "created_at"
        )
        return success_response(data=list(forms), message="Forms retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def get_form_service(request, uuid, include_deleted=False):
    try:
        user = get_user_from_request(request)

        queryset = Form.objects.filter(uuid=uuid)
        if user:
            queryset = queryset.filter(user=user)
        if not include_deleted:
            queryset = queryset.filter(is_deleted=False)

        form = queryset.values().first()
        if not form:
            return error_response("Form not found", status=404)

        return success_response(data=form, message="Form retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)

def get_form_details_service(request, uuid):
    try:
        queryset = Form.objects.filter(uuid=uuid)

        form = queryset.values().first()
        if not form:
            return error_response("Form not found", status=404)

        return success_response(data=form, message="Form retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)

def update_form_service(request, uuid):
    try:
        user = get_user_from_request(request)
        if not user:
            return error_response("User not found", status=401)

        data = json.loads(request.body)
        form = Form.objects.filter(uuid=uuid, user=user, is_deleted=False).first()
        if not form:
            return error_response("Form not found or deleted", status=404)

        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)
        form.save()

        return success_response(message="Form updated successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def delete_form_service(request, uuid):
    try:
        user = get_user_from_request(request)
        if not user:
            return error_response("User not found", status=401)

        form = Form.objects.filter(uuid=uuid, user=user, is_deleted=False).first()
        if not form:
            return error_response("Form not found or already deleted", status=404)

        form.delete()  # Soft delete
        return success_response(message="Form soft-deleted successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def restore_form_service(request, uuid):
    try:
        user = get_user_from_request(request)
        if not user:
            return error_response("User not found", status=401)

        form = Form.objects.filter(uuid=uuid, user=user, is_deleted=True).first()
        if not form:
            return error_response("Form not found or not deleted", status=404)

        form.restore()
        return success_response(message="Form restored successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def toggle_publish_form_service(request, uuid):
    try:
        user = get_user_from_request(request)
        if not user:
            return error_response("User not found", status=401)

        form = Form.objects.filter(uuid=uuid, user=user, is_deleted=False).first()
        if not form:
            return error_response("Form not found or deleted", status=404)

        form.is_public = not form.is_public
        form.save()
        status_text = "published" if form.is_public else "unpublished"
        return success_response(message=f"Form is now {status_text}.", data={"is_public": form.is_public})
    except Exception as e:
        return error_response(message=str(e), status=500)
