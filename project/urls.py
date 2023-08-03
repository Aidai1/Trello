

from django.urls import path
from . import views
from .views import UserDetailView, AddToFavoritesView,CreateColumnView, create_board, create_card, create_column, login, login_required


urlpatterns = [
   path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
   path('board/add_to_favorites/', AddToFavoritesView.as_view(), name='add_to_favorites'),
   path('', views.index, name='index'),  # URL-маршрут для главной страницы приложения
   path('create_board/', views.create_board, name='create_board'),
   path('board/<int:board_id>/', views.board_detail, name='board_detail'),
   path('project/board/<int:board_id>/create_column/', CreateColumnView.as_view(), name='create-column'),
   path('board/<int:board_id>/column/<int:column_id>/create_card/', views.create_card, name='create_card'),
    # Добавьте здесь другие URL-маршруты для остальных действий (обновление, удаление и т.д.).
]



