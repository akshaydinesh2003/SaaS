from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/assign/', views.assign_task, name='assign_task'),
    path('role/request/', views.request_role_change, name='request_role_change'),
    path('role/manage/', views.manage_role_requests, name='manage_role_requests'),
    path('role-request/process/<int:role_request_id>/', views.process_role_request, name='process_role_request'),
]
