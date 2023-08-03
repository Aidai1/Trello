from django import forms 
from .models import CustomUser, Board, Card, Color, Comment, Column, Label, ChecklistItem, Checklist
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password1', 'password2']
            


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'background']
        
        
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'description', 'order', 'due_date', 'labels']
        
class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['title']
        
class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['text'] 
    
class CardLabelForm(forms.ModelForm):
    color = forms.ModelChoiceField(queryset=Color.objects.all(), widget=forms.Select)
    
    class Meta:
        model = Label
        fields = ['name', 'color']
                                    
                        