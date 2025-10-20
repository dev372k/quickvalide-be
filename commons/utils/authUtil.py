# auth_utils.py
import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from apps.user.models import Profile

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)

        #Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE3NTk1ODAwODgsImlhdCI6MTc1OTU3NjQ4OH0.gaGwtCDVtHKLsmO76OfSEhDHbrPah7hmQ9_xix2iqSs
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            
            #will discuss later when working with Product Post/Put APIs
            request.user_id = payload["user_id"]  # attach user_id to request
            request.user = payload["user"]  # attach user_id to request
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)
    return wrapper


def api_key_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            profile = Profile.objects.filter(api_key=token).first()

            if not profile:
                return JsonResponse({"error": "Invalid or unknown API key"}, status=401)

            # ✅ Attach user info to request
            request.user_id = profile.id  # user_id from related user
            request.user = profile         # full user object

        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

        return view_func(request, *args, **kwargs)
    return wrapper
