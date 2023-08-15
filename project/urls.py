from django.urls import path
from project.views.chek_list_view import (
    ChecklistCreateView,
    ChecklistUpdateView,
    ChecklistDeleteView,
    ChecklistItemCreateView,
    ChecklistItemDeleteView,
    ChecklistItemListView
)
from project.views.board_view import (
    BoardIndexView,
    BoardCreateView,
    BoardDetailView,
    BoardUpdateView,
    BoardDeleteView, BoardJoinView
)
from project.views.column_view import (
    ColumnCreateView,
    ColumnDeleteView,
    ColumnDetailView,
    ColumnUpdateView,
)

from project.views.card_view import (
    CardCreateView,
    CardDeleteView,
    CardUpdateView,
    CardDetailView
)

from project.views.comment_view import CommentUpdateView, CommentDeleteView, CommentCreateView
from project.views.label_view import CardLabelCreateView

urlpatterns = [
    path('', BoardIndexView.as_view(), name='index'),
    path('board/<int:pk>/join/', BoardJoinView.as_view(), name='board_join'),
    path('/<int:pk>/', CardDetailView.as_view(), name='detail_card'),
    path('comment/<int:pk>/update', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('card/<int:pk>/comment/add/', CommentCreateView.as_view(), name='card_comment_add'),
    path('card/<int:pk>/label/', CardLabelCreateView.as_view(), name='card_label_create'),
    path('card/<int:pk>/checklist/create/', ChecklistCreateView.as_view(), name='checklist_create'),
    path('checklist/<int:pk>/update/', ChecklistUpdateView.as_view(), name='checklist_update'),
    path('checklist/<int:pk>/delete/', ChecklistDeleteView.as_view(), name='checklist_delete'),
    path('checklist/<int:pk>/item/create/', ChecklistItemCreateView.as_view(), name='checklist_item_create'),
    path('checklist/item/<int:pk>/delete/', ChecklistItemDeleteView.as_view(),
         name='checklist_item_delete'),
    path('checklist/<int:pk>/item/list/', ChecklistItemListView.as_view(),
         name='checklist_item_list'),
    path('board/create/', BoardCreateView.as_view(), name='create_board'),
    path('board/<int:pk>/update/', BoardUpdateView.as_view(), name='update_board'),
    path('board/<int:pk>/delete/', BoardDeleteView.as_view(), name='delete_board'),
    path('board/<int:pk>/column/', BoardDetailView.as_view(), name='list_column'),
    path('column/<int:pk>/create/', ColumnCreateView.as_view(), name='create_column'),
    path('column/delete/<int:pk>/', ColumnDeleteView.as_view(), name='delete_column'),
    path('column/update/<int:pk>/', ColumnUpdateView.as_view(), name='update_column'),
    path('column/detail/<int:pk>/', ColumnDetailView.as_view(), name='detail_column_cards'),
    path('cards/<int:pk>/create/', CardCreateView.as_view(), name='create_card'),
    path('cards/delete/<int:pk>/', CardDeleteView.as_view(), name='delete_card'),
    path('cards/update/<int:pk>/', CardUpdateView.as_view(), name='update_card'),
    path('cards/detail', CardDetailView.as_view(), name='detail_card')

]







    

