from django import forms 
from .models import  Board, Card, Color, Comment, Column, Label, ChecklistItem, Checklist
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets

            


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'background', 'users']
        widgets = {
            'users' : widgets.CheckboxSelectMultiple
        }
        
        
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
                                    

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти',
                             widget=widgets.TextInput(attrs={'class': "form-control w-25"}))

                        