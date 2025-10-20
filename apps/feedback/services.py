import json
import requests
from django.shortcuts import get_object_or_404
from .models import Feedback
from ..form.models import Form
from ..user.models import Profile
from django.db.models import Count
from django.db.models.functions import TruncDate
from commons.utils.jsonUtil import success_response, error_response


def sentiment_analyzer(message, rating):
    """
    Calls external AI API to analyze sentiment, summary, suggestions, and sentiment_score.
    sentiment_score: float between 0 and 1, where 0 = fully negative, 1 = fully positive.
    """
    import json
    import requests

    try:
        url = "https://sharp-gpt.ai/PostAPIRequest"

        payload = json.dumps({
            "inputPrompt": f"message: {message}, rating: {rating}",
            "ChatMessage": [
                {
                    "role": "system",
                    "content": (
                        "You are an advanced AI feedback analyzer. You will receive input like this:\n"
                        "message: message, rating: rating\n\n"
                        "Your job is to analyze both the written message and the numeric rating to determine overall sentiment.\n"
                        "Return ONLY a JSON object with this exact structure:\n\n"
                        "{\n"
                        "  \"sentiment\": \"positive | neutral | negative\",\n"
                        "  \"sentiment_score\": 0.0–1.0,  # strength of positivity or negativity (0=negative, 1=positive)\n"
                        "  \"summary\": \"A one-sentence summary of the feedback\",\n"
                        "  \"suggestions\": [\"List of specific improvements or acknowledgments\"]\n"
                        "}\n\n"
                        "Guidelines:\n"
                        "- Combine message tone and rating.\n"
                        "- If rating ≤ 2 → usually negative, ≥ 4 → usually positive, 3 → neutral, unless message strongly contradicts it.\n"
                        "- sentiment_score should reflect emotional intensity (e.g., 0.1 = very negative, 0.9 = very positive).\n"
                        "- Respond strictly in JSON with no text outside the JSON object."
                    )
                }
            ],
            "userResume": None
        })

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=payload)

        data = json.loads(response.text)
        inner_data = json.loads(data["data"])
        content = inner_data["choices"][0]["message"]["content"]

        # Parse JSON returned by AI
        result = json.loads(content)

        # Validate sentiment_score
        score = result.get("sentiment_score", None)
        if not isinstance(score, (float, int)) or score < 0 or score > 1:
            sentiment = result.get("sentiment", "").lower()
            score = 1.0 if sentiment == "positive" else 0.5 if sentiment == "neutral" else 0.0
            result["sentiment_score"] = round(score, 2)

        return result

    except Exception as e:
        # Fallback in case of any failure
        return {
            "sentiment": "neutral",
            "summary": "Feedback analysis unavailable.",
            "suggestions": [],
            "sentiment_score": 0.5,
            "error": str(e),
        }


def get_user_from_request(request):
    user_id = request.user_id

    if not user_id:
        return None
    return Profile.objects.filter(id=user_id).first()

def create_feedback_service(request):
    try:
        data = json.loads(request.body)
        form_uuid = data.get("form_uuid")
        form = get_object_or_404(Form, uuid=form_uuid, is_deleted=False)

        name = data.get("name")
        message = data.get("message", "")
        rating = int(data.get("rating", 3))
        email = data.get("email")

        # AI Sentiment Analysis
        ai_result = sentiment_analyzer(message, rating)

        feedback = Feedback.objects.create(
            form=form,
            name=name,
            email=email,
            message=message,
            sentiment=ai_result.get("sentiment"),
            sentiment_score=ai_result.get("sentiment_score"),
            summary=ai_result.get("summary"),
            suggestions=ai_result.get("suggestions", []),
            rating=rating,
        )

        return success_response(
            message="Feedback submitted successfully.",
            data={
                "id": feedback.id,
                "sentiment": feedback.sentiment,
                "sentiment_score": feedback.sentiment_score,
                "summary": feedback.summary,
                "suggestions": feedback.suggestions,
            },
        )
    except Exception as e:
        return error_response(message=str(e), status=500)


def list_feedback_by_user_service(request, form_uuid):
    try:
        user = get_user_from_request(request)
        form = get_object_or_404(Form, uuid=form_uuid, user=user, is_deleted=False)
        feedbacks = form.feedbacks.filter(is_deleted=False).values(
            "id", "name", "email", "message", "sentiment", "sentiment_score", "suggestions", "rating", "created_at"
        )
        return success_response(data=list(feedbacks), message="Feedback list retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)

def list_feedback_by_form_service(request, form_uuid):
    try:
        form = get_object_or_404(Form, uuid=form_uuid, is_deleted=False)
        feedbacks = form.feedbacks.filter(is_deleted=False, sentiment="positive").values(
            "id", "name", "email", "message", "sentiment", "sentiment_score", "suggestions", "rating", "created_at"
        )
        return success_response(data=list(feedbacks), message="Feedback list retrieved successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)


def delete_feedback_service(request, feedback_id):
    try:
        user = get_user_from_request(request)
        feedback = Feedback.objects.filter(id=feedback_id, form__user=user, is_deleted=False).first()
        if not feedback:
            return error_response("Feedback not found", status=404)

        feedback.delete()
        return success_response(message="Feedback deleted successfully.")
    except Exception as e:
        return error_response(message=str(e), status=500)
    
def feedback_count_service(request, form_uuid):
    feedback_counts = (
        Feedback.objects
        .filter(uuid=form_uuid)
        .annotate(date=TruncDate('sentiment'))  # assuming BaseModel has created_at
        .values('date')
        .annotate(count=Count('id'))
        .order_by('-sentiment')
    )

    return success_response(list(feedback_counts))