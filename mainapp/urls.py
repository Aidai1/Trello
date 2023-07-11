from django.urls import path
from .views import (
   BoardCreateView,
   BoardDeletView,
   BoardDetailView,
   BoardUpdateView,  
   
)

urlpatterns = [
    path('board/create/', BoardCreateView.as_view(), name='create_board'),
    path('board/<int:pk>/update/', BoardUpdateView.as_view(), name='update_board'),
    path('board/<int:pk>/delete/', BoardDeletView.as_view(), name='delete_board'),
    path('board/<int:pk>/column/', BoardDetailView.as_view(), name='list_column'),
    
]
