import json
from django.utils.text import slugify
from models import Form
from commons.utils.jsonUtil import success_response, error_response

def create_form_service(request, user):
    try:
        data = json.loads(request.body)
        title = data.get("title")
        if not title:
            return error_response("Title is required", status=400)

        slug = slugify(title)
        # Ensure unique slug
        if Form.objects.filter(slug=slug).exists():
            slug = f"{slug}-{Form.objects.count() + 1}"

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
            data={"uuid": str(form.uuid), "title": form.title, "slug": form.slug},
        )

    except Exception as e:
        return error_response(message=str(e), status=500)


def list_forms_service(request, user):
    try:
        forms = Form.objects.filter(user=user).values(
            "uuid", "title", "description", "slug", "is_public", "created_at"
        )
        return success_response(data=list(forms), message="Forms retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def get_form_service(request, uuid):
    try:
        form = Form.objects.filter(uuid=uuid).values().first()
        if not form:
            return error_response("Form not found", status=404)
        return success_response(data=form, message="Form retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def update_form_service(request, uuid, user):
    try:
        data = json.loads(request.body)
        form = Form.objects.filter(uuid=uuid, user=user).first()
        if not form:
            return error_response("Form not found or unauthorized", status=404)

        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)
        form.save()

        return success_response(message="Form updated successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def delete_form_service(request, uuid, user):
    try:
        form = Form.objects.filter(uuid=uuid, user=user).first()
        if not form:
            return error_response("Form not found or unauthorized", status=404)

        form.delete()
        return success_response(message="Form deleted successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)
