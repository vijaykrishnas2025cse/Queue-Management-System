from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:queue_id>/', views.book_token, name='book_token'),
    path('token/<int:token_id>/', views.token_detail, name='token_detail'),
    path('token/<int:token_id>/cancel/', views.cancel_token, name='cancel_token'),
    path('tokens/', views.token_list, name='token_list'),
    path('api/token-position/<int:token_id>/', views.token_api_position, name='token_api_position'),
    path('rewards/', views.reward_dashboard, name='reward_dashboard'),
    path('reward-graph/', views.reward_graph, name='reward_graph'),
    path('reward-list/', views.reward_list, name='reward_list'),
    path('verify-qr/', views.verify_qr_completion, name='verify_qr_completion'),
]
