import json
import jwt
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.conf import settings 
from .models import Profile
import uuid
from commons.utils.jsonUtil import success_response, error_response

plan = [{
     "id": 1,
     "name": "starter",
     "allowed_form_count": 1
},{
     "id": 2,
     "name": "boost",
     "allowed_form_count": 5
},{
     "id": 3,
     "name": "infinity",
     "allowed_form_count": 100,
}]


def create_user_service(request):
    data = json.loads(request.body)
    hashed = make_password(data.get("password"))
    Profile.objects.create(username=data.get("username"), password=hashed,email =data.get("email"),first_name=data.get('first_name'),last_name=data.get('last_name'), plan = plan[0])
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
                    "email": user.email,
                    "plan": user.plan,
                    "api_key": uuid.uuid4().hex,
                    "api_key_limit": 0,
                },
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
                "iat": datetime.datetime.utcnow(),
            }

            token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

            return success_response(data={"token": token, "user" : {"id" : user.id,  "name" : f"{user.first_name} {user.last_name}","email" : user.email}}, message="Login successful.")
    
        except Exception as e:
            return error_response(message=str(e), status=500)
        

def change_user_password(request):
     data =json.loads(request.body)
     user = authenticate(username = request.username, password = data.get('Old_password'))
     if user is not None:
          if(data.get('New_password')) == data.get('Confirm_password'):
               user.set_password(data.get('New_password'))
               user.save()
               return success_response(message="Password changed successfully")
          else:
               return error_response(message="Please make sure both passwords are the same.")
     else:
          return error_response(message="Incorrect password.")


def update_user(request,):
     try:
          user = Profile.objects.get(id=request.user_id)
     except Profile.DoesNotExist:
          return error_response(message=f"this user {request.user_id} is not present.")
          
     data = json.loads(request.body)
     user.username = data.get('username')
     user.email = data.get('email')
     user.first_name = data.get('first_name')
     user.last_name = data.get('last_name')
     user.save()
     return success_response(message="User updated successfully.")

def delete_user(reuqest,user_id):
     try:
        user = Profile.objects.get(id=user_id)
     except:
        return error_response(message=f"this user {user_id} is not in the database.")
     user.delete()
     return success_response(message="User deleted successfully.")
     