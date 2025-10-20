from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_feedback, name='create_feedback'),
    path('list/<uuid:form_uuid>/', views.list_feedback_by_user, name='list_feedback_by_user'),
    path('list/<uuid:form_uuid>/widget/', views.list_feedback_by_form, name='list_feedback'),
    path('delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback')
]
