from django.urls import path
from . import views

urlpatterns = [
    path('feedbacks/create/', views.create_feedback, name='create_feedback'),
    path('feedbacks/list/<uuid:form_uuid>/', views.list_feedback_by_form, name='list_feedback'),
    path('feedbacks/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

    # API Logs work
    path('logs/', views.list_apilogs_by_user_service, name='list_apilogs_by_user_service'),
    path('logs/graph', views.api_call_count_per_day, name='api_call_count_per_day'),
]
