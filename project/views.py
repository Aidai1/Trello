
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import User, Board, Card, Checklist, ChecklistItem, Color, Column, Comment, Label,User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from .forms import UserForm, RegistrationForm, BoardForm, CardForm, ChecklistForm, ColumnForm, CommentForm, CardLabelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token

class UserDetailView(DetailView, ListView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    
    def post(self, request, *args, **kwargs):
        board = self.get_object()
        request.user.add_to_favorites(board)
        return HttpResponseRedirect(self.request.path)

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        return user == self.request.user



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
            


class LoginView(DetailView, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    
   
    
class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'colum/list_colum.html'
    context_object_name = 'board'
    
    def post(self, request, *args, **kwargs):
        board = self.get_object()
        board.favorite_boards.add(request.user)
        return redirect('list_colum', id=board.id)
    
class BoardUpdateView(PermissionRequiredMixin, UpdateView):
    model = Board
    form_class = BoardForm  
    temlate_name = 'boards/update_board.html'
    context_object_name = 'boards'
    success_url = reverse_lazy('index')
    permission_required = 'trelloapp.update_view'
    
    def has_permission(self) -> bool:
        return super().has_permission() or self.get_object().author == self.request.user   
    

class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    context_object_name = 'board'
    template_name = 'board/create_board.html'
    form_class = BoardForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        board = form.save(commit=False)
        board.author = self.request.user
        board.save()
        board.users.set(form.cleaned_data['users'])
        return super().form_valid(form)
    
class BoardDeletView(PermissionRequiredMixin, DeleteView):
    model = Board
    template_name = 'boards/delete_board.html'
    context_object_name = 'boards'
    success_url = reverse_lazy('index')
    permission_required = 'trelloapp.delete_board'
    
    def has_permission(self) -> bool:
        return super().has_permission() or self.get_object().author == self.request.user    
    
    
class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "cards/create_card.html"
    context_object_name = "card"
    form_class = CardForm
    
class CardDetailView(PermissionRequiredMixin, DetailView):
    model = Card
    template_name = "card/detail_card.html" 
    permission_required = "app.view_app"
    
class CardUpdateView(PermissionRequiredMixin, UpdateView):
    model = Card
    template_name = 'cards/update_card.html'
    success_uls = reverse_lazy('index')
    
class CardDeleteView(DeleteView):
    model = Card
    template_name = "cards/delete_card.html"
    success_url = reverse_lazy('index')
    
class ChecklistCreateView(CreateView):
    model = Checklist
    template_name = "checlist/checlist_create.html"
    form_class = ChecklistForm
    
class ChecklistUpdateView(PermissionRequiredMixin, UpdateView):
    model = Checklist
    template_name = "checklist/checklist_update.html"
    form_class = ChecklistForm
    context_object_name = "checklists"
    
class ChecklistDeletView(DeleteView):
    model = Checklist
    
    
class ChecklistItemListView(ListView):
    model = ChecklistItem
    template_name = 'checklist/item_list.html'
    context_object_name = "items"   
    

class ColumnListView(PermissionRequiredMixin, ListView):
    model = Column
    template_name = "column/list_colum.html"
    context_object_name = "colum"
    
class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    template_name = "column/create_colum.html"
    context_object_name = "columns"
    form_class = ColumnForm
    
class ColumnUpdateView(PermissionRequiredMixin, UpdateView):
    model = Column
    context_object_name = "columns"
    
    
class ColumnDeleteView(PermissionRequiredMixin, DeleteView):
    model = Column
    temlate_name = "column/delete_column.html"
    success_url = reverse_lazy('detail_colum')
    context_object_name = "columns"
    
    
class ColumnDetailView(PermissionRequiredMixin, DetailView):
    model = Column
    template_name = 'column/detail_column_cards.html'
    context_object_name = "columns"
    
    
                     
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment 
    template_name = 'comment/create_comment.html'
    form_class = CommentForm
    
    
class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = "comment/update_comment.html"
    form_class = CommentForm
    context_object_name = "comment"
    
    
class CommentDeleteView(DeleteView):
    model = Comment
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    
class CardLabelCreateView(CreateView):
    model = Label
    form_class = CardLabelForm   
    template_name = "label/label_create.html"
     
     
   