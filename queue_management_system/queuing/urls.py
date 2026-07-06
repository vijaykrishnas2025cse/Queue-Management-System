from django.urls import path
from . import views

urlpatterns = [
    # User views
    path('list/', views.queue_list, name='queue_list'),
    path('<int:queue_id>/', views.queue_detail, name='queue_detail'),
    path('api/status/<int:queue_id>/', views.queue_api_status, name='queue_api_status'),
    
    # Admin views
    path('admin/list/', views.admin_queue_list, name='admin_queue_list'),
    path('admin/create/', views.admin_queue_create, name='admin_queue_create'),
    path('admin/<int:queue_id>/update/', views.admin_queue_update, name='admin_queue_update'),
    path('admin/<int:queue_id>/detail/', views.admin_queue_detail, name='admin_queue_detail'),
    path('admin/<int:queue_id>/serve-next/', views.admin_serve_next, name='admin_serve_next'),
    path('admin/<int:queue_id>/verify-qr/', views.admin_verify_qr, name='admin_verify_qr'),
]
