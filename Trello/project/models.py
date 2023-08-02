from django.db import models
from django.contrib.auth import get_user_model

from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, blank=True)
   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    
class Board(models.Model):
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, verbose_name="Автор"
                               , related_name="author_project")
    users = models.ManyToManyField(get_user_model(), verbose_name="Участники", related_name='boards_users')
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название")
    background = models.ImageField(upload_to='board_backgrounds/', null=True, blank=True, verbose_name="Фон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    arhiv = models.BooleanField(default=False, verbose_name="В архиве")
    
    def __str__(self) -> str:
        return self.title
    
    
    
class Color(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=8)  
    
    def __str__(self) -> str:
        return self.name
    

class Label(models.Model):
    name = models.CharField(max_length=30)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    
    
    
class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=30, null=False, blank=False)
    order = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title   
    
class Card(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    due_date = models.DateField(null=True, blank=True) 
    labels = models.ManyToManyField(Label, related_name='cards_label', blank=True)
    
    
    def __str__(self) -> str:
        return self.title
    
class Checklist(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1,verbose_name='Автор чеклиста')   
    
    def __str__(self):
        return self.title


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=300, null=False, blank=False)
    author = models.CharField(max_length=50,verbose_name="Автор комментария")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text    

