from django import forms 
from .models import Board, Card, Color, Comment, Column, Label, ChecklistItem, Checklist


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'background', 'users']
        widgets = {
            'users : widgets.CheckboxSelectMultiple',
        }
        
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'description', 'order', 'due_date', 'labels']
        
class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title']
        
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
        
# class SimplSearchForm(forms.ModelForm):
#     search = forms.CharField(max_length=100, required=False, label='Find',
#                              widget=widjets.TextInput(attrs={'class': "form-control w-2500"}))                                       
                        