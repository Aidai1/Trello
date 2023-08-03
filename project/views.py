from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Board, Column, Card, Comment, Checklist, ChecklistItem, Label
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
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

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
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')




# Вспомогательная функция для проверки авторизации пользователя
def is_user_authenticated(user):
    return user.is_authenticated

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

    return render(request, 'create_board.html')



@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    participants = board.participants.all()
    recently_viewed_boards = request.user.boards.order_by('-id')[:6]
    all_labels = Label.objects.all()
    favorite_boards = request.user.boards.filter(is_archived=False)

    return render(request, 'board_detail.html', {
        'board': board,
        'participants': participants,
        'recently_viewed_boards': recently_viewed_boards,
        'all_labels': all_labels,
        'favorite_boards': favorite_boards,
    })

@login_required
def create_column(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        # Обработка данных, полученных из формы создания колонки
        name = request.POST.get('name')

        # Проверка наличия обязательных данных
        if name:
            new_column = Column.objects.create(board=board, name=name)
            return redirect('board_detail', board_id=board.id)
        else:
            error_message = "Необходимо указать название колонки."
            return render(request, 'create_column.html', {'board': board, 'error_message': error_message})

    return render(request, 'create_column.html', {'board': board})

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

            return redirect('board_detail', board_id=board_id)
        else:
            error_message = "Необходимо указать название карточки."
            return render(request, 'create_card.html', {'column': column, 'error_message': error_message})

    labels = Label.objects.all()
    return render(request, 'create_card.html', {'column': column, 'labels': labels})


class AddToFavoritesView(View):
    def post(self, request, *args, **kwargs):
        board_id = request.POST.get('board_id')
        board = Board.objects.get(id=board_id)
        request.user.add_to_favorites(board)
        return redirect('list_column', pk=board_id)