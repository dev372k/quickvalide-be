from django.urls import path
from . import views

urlpatterns =[
    path('login',views.login,name= "login"),
    path('me',views.get,name= "login"),
    path('register',views.create,name= "login"),
    path('change-password',views.change_password,name= "change_password"),
    path('update',views.update,name= "update_user"),
    path('update/key',views.update_key,name= "update_user_api_key"),
    path('get/key',views.get_key,name= "get_user_api_key"),
    path('delete/<int:user_id>',views.delete,name= "delete_user"),
    path('restore/<int:user_id>',views.restore,name= "restore_user"),
]