from django.contrib.auth.models import User
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

