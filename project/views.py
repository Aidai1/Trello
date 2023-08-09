from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser, Board, Card, Checklist,ChecklistItem, Color,Column, Comment, Label
from django.urls import reverse_lazy, reverse
from .forms import BoardForm, ColumnForm, CardForm, CardLabelForm, ChecklistItemForm, CommentForm, CardLabelForm, UserRegistrationForm,ChecklistForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.views import View

def index(request):
    return render(request, 'index.html')



User = get_user_model()

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'  
    context_object_name = 'user'

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    # else:
    #     form = UserRegistrationForm()
    # return render(request, 'registration/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with the URL name of your main user dashboard page
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'user/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def is_user_authenticated(user):
    return user.is_authenticated
        



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
   


class AddToFavoritesView(View):
    def post(self, request, *args, **kwargs):
        board_id = request.POST.get('board_id')
        board = Board.objects.get(id=board_id)
        request.user.add_to_favorites(board)
        return redirect('list_column', pk=board_id)
    
    
@login_required
def toggle_favorite_board(request, board_id):
    user_profile = User.objects.get(user=request.user)
    board = Board.objects.get(id=board_id)
    if board in user_profile.favorite_boards.all():
        user_profile.favorite_boards.remove(board)
    else:
        user_profile.favorite_boards.add(board)
    return redirect('favorite_boards')   









class BoardIndexView(LoginRequiredMixin, ListView):
    model = Board
    template_name = 'board/index.html'
    context_object_name = 'board'


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board/create_board.html'
    form_class = BoardForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        board = form.save(commit=False)
        board.author = self.request.user
        board.save()
        board.users.set(form.cleaned_data['users'])
        return super().form_valid(form)

class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'column/list_column.html'
    context_object_name = 'board'

    def post(self, request, *args, **kwargs):
        board = self.get_object()
        board.favorite_boards.add(request.user)
        return redirect('list_column', id=board.id)


class BoardUpdateView(PermissionRequiredMixin, UpdateView):
    model = Board
    form_class = BoardForm
    template_name = 'board/update_board.html'
    context_object_name = 'boards'
    success_url = reverse_lazy('index')
    permission_required = 'project.update_view'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user



class BoardDeleteView(PermissionRequiredMixin, DeleteView):
    model = Board
    template_name = 'board/delete.html'
    context_object_name = 'boards'
    success_url = reverse_lazy('index')
    permission_required = 'project.delete_board'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user




@login_required
def create_board(request):
    if request.method == 'POST':
        # Обработка данных, полученных из формы создания доски
        title = request.POST.get('title')
        background = request.FILES.get('background')

        # Проверка наличия обязательных данных
        if title and background:
            new_board = Board.objects.create(title=title, background=background)
            new_board.participants.add(request.user)  # Добавляем текущего пользователя как участника
            return redirect('board_detail', board_id=new_board.id)
        else:
            error_message = "Необходимо указать заголовок и загрузить фоновое изображение."
            return render(request, 'create_board.html', {'error_message': error_message})

    return render(request, 'board/create_board.html')



# @login_required
# def board_detail(request, board_id):
#     board = get_object_or_404(Board, pk=board_id)
#     participants = board.participants.all()
#     recently_viewed_boards = request.user.boards.order_by('-id')[:6]
#     all_labels = Label.objects.all()
#     favorite_boards = request.user.boards.filter(is_archived=False)

#     return render(request, 'board_detail.html', {
#         'board': board,
#         'participants': participants,
#         'recently_viewed_boards': recently_viewed_boards,
#         'all_labels': all_labels,
#         'favorite_boards': favorite_boards,
#     })



class ColumnListView(PermissionRequiredMixin, ListView):
    template_name = 'column/list_column.html'
    context_object_name = 'columns'
    model = Column
    permission_required = 'project.view_column'

    def has_permission(self):
        board_ids = self.model.objects.values_list('board_id', flat=True)
        participant_boards = Board.objects.filter(users=self.request.user, id__in=board_ids)
        return participant_boards.exists()
    
    

@login_required
def create_column(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        # Обработка данных, полученных из формы создания колонки
        name = request.POST.get('name')

        # Проверка наличия обязательных данных
        if name:
            new_column = Column.objects.create(board=board, name=name)
            return redirect('create_board', board_id=board.id)
        else:
            error_message = "Необходимо указать название колонки."
            return render(request, 'create_column.html', {'board': board, 'error_message': error_message})

    return render(request, 'create_column.html', {'board': board})



class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    template_name = "column/create_column.html"
    context_object_name = "colomns"
    form_class = ColumnForm

    def get_success_url(self):
        return reverse('list_column', kwargs={'pk': self.object.board.pk})

    def form_valid(self, form):
        board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        form.instance.board = board
        return super().form_valid(form)




class ColumnUpdateView(UpdateView):
    model = Column
    success_url = reverse_lazy('index')
    context_object_name = "columns"
    

    def has_permission(self):
        if self.request.user == self.get_object().board.author:
            return True
        return False


class ColumnDeleteView(DeleteView):
    model = Column
    template_name = "column/delete_column.html"
    success_url = reverse_lazy('detail_column')
    context_object_name = "columns"
  

    def has_permission(self):
        if self.request.user == self.get_object().board.author:
            return True
        return False

class ColumnDetailView(DetailView):
    model = Column
    context_object_name = "columns"
    template_name = "column/detail_column_cards.html"
   

    def has_permission(self):
        board = self.get_object().board
        return board.users.filter(id=self.request.user.id).exists()





@login_required
def create_card(request, board_id, column_id):
    column = get_object_or_404(Column, pk=column_id)

    if request.method == 'POST':
        # Обработка данных, полученных из формы создания карточки
        name = request.POST.get('name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        labels = request.POST.getlist('labels')

        # Проверка наличия обязательных данных
        if name:
            new_card = Card.objects.create(column=column, name=name, description=description, due_date=due_date)

            # Добавляем метки к карточке
            for label_id in labels:
                label = get_object_or_404(Label, pk=label_id)
                new_card.labels.add(label)

            return redirect('create_board', board_id=board_id)
        else:
            error_message = "Необходимо указать название карточки."
            return render(request, 'create_card.html', {'column': column, 'error_message': error_message})

    labels = Label.objects.all()
    return render(request, 'create_card.html', {'column': column, 'labels': labels})


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "cards/create.html"
    context_object_name = "cards"
    form_class = CardForm

    def get_success_url(self):
        return reverse('detail_column_cards', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        card = get_object_or_404(Column, pk=self.kwargs.get('pk'))
        form.instance.column = card
        return super().form_valid(form)
    
    
class CardDetailView(PermissionRequiredMixin, DetailView):
    model = Card
    template_name = 'cards/detail_card.html'
    permission_required = 'project.view_card'

    def has_permission(self):
        board = self.get_object().column.board
        return board.users.filter(id=self.request.user.id).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = self.object
        comments = card.comments.order_by('-created_at')
        context['comments'] = comments
        checklists = Checklist.objects.filter(card=card)
        context['checklists'] = checklists
        return context


class CardUpdateView(PermissionRequiredMixin, UpdateView):
    model = Card
    template_name = 'cards/update_card.html'
    success_url = reverse_lazy('index')



class CardDeleteView(DeleteView):
    model = Card
    template_name = 'cards/delete_card.html'
    success_url = reverse_lazy('index')    


class ChecklistCreateView(CreateView):
    model = Checklist
    template_name = 'checklist/create_cheklist.html'
    form_class = ChecklistForm

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk})

    def form_valid(self, form):
        card = get_object_or_404(Card, pk=self.kwargs.get('pk'))
        form.instance.card = card
        return super().form_valid(form)


class ChecklistUpdateView(PermissionRequiredMixin, UpdateView):
    model = Checklist
    template_name = 'checklist/update_checklist.html'
    form_class = ChecklistForm
    context_object_name = 'checklists'

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk})

    def has_permission(self):
        return self.request.user.has_perm('project.change_checklist') or self.get_object().author == self.request.user


class ChecklistDeleteView(DeleteView):
    model = Checklist

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.has_perm('project.delete_checklist') or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk })

class ChecklistItemCreateView(CreateView):
    model = ChecklistItem
    template_name = 'checklist/item_create.html'
    form_class = ChecklistItemForm

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        checklist = get_object_or_404(Checklist, pk=self.kwargs['pk'])
        form.instance.card = checklist
        return super().form_valid(form)




class ChecklistItemDeleteView(UserPassesTestMixin, DeleteView):
    model = ChecklistItem

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.has_perm('project.delete_checklistitem')\
               or self.get_object().cheklist.author == self.request.user

    def get_success_url(self):
        checklist = self.object.checklist
        return reverse('checklist_item_list', kwargs={'pk': checklist.pk})


class ChecklistItemListView(ListView):
    model = ChecklistItem
    template_name = 'checklist/item_list.html'
    context_object_name = 'items'


class ColumnListView(PermissionRequiredMixin, ListView):
    template_name = 'column/list_column.html'
    context_object_name = 'columns'
    model = Column
    permission_required = 'project.view_column'

    def has_permission(self):
        board_ids = self.model.objects.values_list('board_id', flat=True)
        participant_boards = Board.objects.filter(users=self.request.user, id__in=board_ids)
        return participant_boards.exists()


class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    template_name = "column/create_column.html"
    context_object_name = "colomns"
    form_class = ColumnForm

    def get_success_url(self):
        return reverse('list_column', kwargs={'pk': self.object.board.pk})

    def form_valid(self, form):
        board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        form.instance.board = board
        return super().form_valid(form)


class ColumnUpdateView(PermissionRequiredMixin, UpdateView):
    model = Column
    success_url = reverse_lazy('index')
    context_object_name = "columns"
    permission_required = 'project.change_column'

    def has_permission(self):
        if self.request.user == self.get_object().board.author:
            return True
        return False



class ColumnDeleteView(PermissionRequiredMixin, DeleteView):
    model = Column
    template_name = "column/delete_column.html"
    success_url = reverse_lazy('detail_column')
    context_object_name = "columns"
    permission_required = 'project.delete_column'

    def has_permission(self):
        if self.request.user == self.get_object().board.author:
            return True
        return False


class ColumnDetailView(PermissionRequiredMixin, DetailView):
    model = Column
    context_object_name = "columns"
    template_name = "column/detail_column_cards.html"
    permission_required = 'project.view_column'

    def has_permission(self):
        board = self.get_object().board
        return board.users.filter(id=self.request.user.id).exists()


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comment/create_comment.html'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk})

    def form_valid(self, form):
        card = get_object_or_404(Card, pk=self.kwargs.get('pk'))
        form.instance.card = card
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comment/update_comment.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def has_permission(self):
        return self.request.user.has_perm('project.change_comment') or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk})



class CardLabelCreateView(CreateView):
    model = Label
    form_class = CardLabelForm
    template_name = 'project/label_create.html'
    success_url = reverse_lazy('card_label_list')


def card_label_create_view(request):
    if request.method == 'POST':
        form = CardLabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('card_label_list')  
    else:
        form = CardLabelForm()

    return render(request, 'project/cardlabel_create.html', {'form': form})




