from django.urls import path
from .views import (
    activate,
    AddToFavoritesView,
    UserDetailView,
    BoardCreateView,
    BoardDeleteView,
    BoardDetailView,
    BoardIndexView,
    BoardUpdateView,
    CardCreateView,
    CardDeleteView,
    CardDetailView,
    CardUpdateView,
    ColumnCreateView,
    ColumnDeleteView,
    ColumnDetailView,
    ColumnUpdateView,
    ChecklistCreateView,
    ChecklistDeleteView,
    ChecklistUpdateView,
    ChecklistItemListView,
    ChecklistItemCreateView,
    ChecklistItemDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CardLabelCreateView,
)

from django.contrib.auth.views import LoginView, LogoutView


app_name = 'project/'

urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('create/', signup, name='signup'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail_account'),
    path('board/add_to_favorites/', AddToFavoritesView.as_view(), name='add_to_favorites'),
    # path('recently_viewed_boards/', recently_viewed_boards, name='recently_viewed_boards'),
    
]

urlpatterns = [
    path('board/create/', BoardCreateView.as_view(), name='board-create'),
    path('board/<int:pk>/delete/', BoardDeleteView.as_view(), name='board-delete'),
    path('board/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('boards/', BoardIndexView.as_view(), name='board-index'),
    path('board/<int:pk>/update/', BoardUpdateView.as_view(), name='board-update'),

]

urlpatterns = [
    path('card/create/', CardCreateView.as_view(), name='card-create'),
    path('card/<int:pk>/delete/', CardDeleteView.as_view(), name='card-delete'),
    path('card/<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('card/<int:pk>/update/', CardUpdateView.as_view(), name='card-update'),
]

urlpatterns = [
    path('column/create/', ColumnCreateView.as_view(), name='column-create'),
    path('column/<int:pk>/delete/', ColumnDeleteView.as_view(), name='column-delete'),
    path('column/<int:pk>/', ColumnDetailView.as_view(), name='column-detail'),
    path('column/<int:pk>/update/', ColumnUpdateView.as_view(), name='column-update'),
]
    

urlpatterns = [
    path('checklist/create/', ChecklistCreateView.as_view(), name='checklist-create'),
    path('checklist/<int:pk>/delete/', ChecklistDeleteView.as_view(), name='checklist-delete'),
    path('checklist/<int:pk>/update/', ChecklistUpdateView.as_view(), name='checklist-update'),
]   

urlpatterns = [
    path('checklist/<int:pk>/items/', ChecklistItemListView.as_view(), name='checklist-items'),
    path('checklist-item/create/', ChecklistItemCreateView.as_view(), name='checklist-item-create'),
    path('checklist-item/<int:pk>/delete/', ChecklistItemDeleteView.as_view(), name='checklist-item-delete'),
    path('comment/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('card-label/create/', CardLabelCreateView.as_view(), name='card-label-create'),
]

    

