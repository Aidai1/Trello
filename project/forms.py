from django import forms 
from .models import User, Board, Card, Color, Comment, Column, Label, ChecklistItem, Checklist
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Requiered')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

            

class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label='Password')
    last_name = forms.CharField(label='Last name')
    
    def email(self):
        email = self.cleaned_data['email']
        return email
    
    def password(self):
        password = self.changed_data['password']
        
    def last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name
    
        


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'background', 'users']
        
        
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
                                    
                        