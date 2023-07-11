from django.contrib import admin
from .models import Board, Card, Color, Column, Comment, Label, Checklist, ChecklistItem, User

admin.site.register(Board) 
admin.site.register(Color) 
admin.site.register(Card) 
admin.site.register(Column) 
admin.site.register(Label) 
admin.site.register(Comment) 
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(User)