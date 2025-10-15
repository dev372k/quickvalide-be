from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_form, name='create_form'),
    path('list/', views.list_forms, name='list_forms'),
    path('<uuid:uuid>/', views.get_form, name='get_form'),
    path('<uuid:uuid>/update/', views.update_form, name='update_form'),
    path('<uuid:uuid>/delete/', views.delete_form, name='delete_form'),
    path('<uuid:uuid>/restore/', views.restore_form, name='restore_form'),
    path('<uuid:uuid>/toggle-publish/', views.toggle_publish_form, name='toggle_publish_form'),
]
