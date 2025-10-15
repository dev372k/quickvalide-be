from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_feedback, name='create_feedback'),
    path('list/<uuid:form_uuid>/', views.list_feedback, name='list_feedback'),
    path('delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
]
