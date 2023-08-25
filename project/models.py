
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import  AbstractUser




class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, blank=True)
    recently_viewed_boards = models.ManyToManyField('project.Board', related_name='recently_viewed_by')
    favorite_boards = models.ManyToManyField('project.Board', related_name='favorited_by')

    def add_to_favorites(self, board):
        self.favorite_boards.add(board)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    


class Board(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_boards',
        verbose_name="Автор"
    )
    users = models.ManyToManyField(
        get_user_model(),
        related_name='boards_users',
        verbose_name="Участники"
    )

    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название")
    background = models.ImageField(upload_to='board_backgrounds/', null=True, blank=True, verbose_name="Фон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    archived = models.BooleanField(default=False, verbose_name="В архиве")


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list_column', kwargs={'pk': self.pk})


class Column(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    order = models.PositiveIntegerField(default=0)
 
    def __str__(self):
        return self.name
 
class Card(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
    due_date = models.DateField(null=True, blank=True)
    labels = models.ManyToManyField('Label', blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=300, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='comments',
                               verbose_name="Автор комментария")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text

class Color(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
    

class Label(models.Model):
    name = models.CharField(max_length=30)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Checklist(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='checklists')
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1,
                               related_name='checklist_author',
                               verbose_name="Автор чеклиста")

    def __str__(self):
        return self.title


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text       
    
    



        