import json
import jwt
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.conf import settings 
from .models import Profile
from commons.utils.jsonUtil import success_response, error_response

def create_user_service(request):
    data = json.loads(request.body)
    hashed = make_password(data.get("password"))
    Profile.objects.create(username=data.get("username"), password=hashed,email =data.get("email"),first_name=data.get('first_name'),last_name=data.get('last_name'))
    return success_response(message="User registered successfully.")
       
def login_user_service(request):
        try:
            data = json.loads(request.body)
            username = data.get("username") 
            password = data.get("password")

            user = authenticate(username=username, password=password)
            if user is None:
                return error_response(message="Invalid credentials", status=401)
            
            payload = {
                "user_id": user.id,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email
                },
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
                "iat": datetime.datetime.utcnow(),
            }

            token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

            return success_response(data={"token": token, "user" : {"id" : user.id,  "name" : f"{user.first_name} {user.last_name}","email" : user.email}}, message="Login successful.")
    
        except Exception as e:
            return error_response(message=str(e), status=500)