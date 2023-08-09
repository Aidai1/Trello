from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
   
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class Board(models.Model):
    title = models.CharField(max_length=100)
    background = models.ImageField(upload_to='board_backgrounds/')
    participants = models.ManyToManyField(CustomUser, related_name='boards')
    # is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

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
    text = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1,
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
    
    


    