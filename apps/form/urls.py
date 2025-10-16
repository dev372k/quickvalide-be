from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_form, name='create_form'),
    path('list/', views.list_forms, name='list_forms'),
    path('<uuid:uuid>/', views.get_form, name='get_form'),
    path('update/<uuid:uuid>/', views.update_form, name='update_form'),
    path('delete/<uuid:uuid>/', views.delete_form, name='delete_form'),
    path('restore/<uuid:uuid>/', views.restore_form, name='restore_form'),
    path('toggle-publish/<uuid:uuid>/', views.toggle_publish_form, name='toggle_publish_form'),
]
