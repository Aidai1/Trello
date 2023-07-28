from django.urls import path
from project import views

from  .views import (
   activate,
   LoginView,
   UserDetailView,
   BoardCreateView,
   BoardDeletView,
   BoardDetailView,
   BoardUpdateView,  
   ColumnCreateView,
   ColumnDeleteView,
   ColumnDetailView,
   ColumnUpdateView,
   CardCreateView,
   CardDeleteView,
   CardDetailView,
   CardUpdateView,
   CommentCreateView,
   CommentDeleteView,
   CommentUpdateView,
   CardLabelCreateView,
   ChecklistDeletView,
   ChecklistItemListView,
   ChecklistUpdateView,
   ChecklistCreateView,
   
)


app_name = 'project/'

urlpatterns = [
   path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
   path('<int:pk>/', UserDetailView.as_view(), name='detail_account'),
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   path('boards/create/', BoardCreateView.as_view(), name='create_board'),
   path('boards/<int:pk>/update/', BoardUpdateView.as_view(), name='update_board'),
   path('boards/<int:pk>/delete/', BoardDeletView.as_view(), name='delete_board'),
   path('boards/<int:pk>/column/', BoardDetailView.as_view(), name='list_column'),
   path('column/<int:pk>/create/', ColumnCreateView.as_view(), name='create_column'),
   path('column/delete/<int:pk>/', ColumnDeleteView.as_view(), name='delete_column'),
   path('column/update/<int:pk>/', ColumnUpdateView.as_view(), name='update_column'),
   path('column/detail/<int:pk>/', ColumnDetailView.as_view(), name='detail_column_cards'),
   path('cards/<int:pk>/create/', CardCreateView.as_view(), name='create_card'),
   path('cards/delete/<int:pk>/', CardDeleteView.as_view(), name='delete_card'),
   path('cards/update/<int:pk>/', CardUpdateView.as_view(), name='update_card'),
   path('cards/detail/<int:pk>/', CardDetailView.as_view(), name='detail_card'),
   path('comment/<int:pk>/update', CommentUpdateView.as_view(), name='comment_update'),
   path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
   path('card/<int:pk>/comment/add/', CommentCreateView.as_view(), name='card_comment_add'),
   path('card/<int:pk>/label/', CardLabelCreateView.as_view(), name='card_label_create'),
   path('card/<int:pk>/checklist/create/', ChecklistCreateView.as_view(), name='checklist_create'),
   path('checklist/<int:pk>/update/', ChecklistUpdateView.as_view(), name='checklist_update'),
   path('checklist/<int:pk>/delete/', ChecklistDeletView.as_view(), name='checklist_delete'),
   path('checklist/<int:pk>/item/list/', ChecklistItemListView.as_view(),
         name='checklist_item_list'),
]
