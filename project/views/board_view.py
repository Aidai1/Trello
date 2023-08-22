from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from project.models import Board
from project.forms import BoardForm, SimpleSearchForm
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views import View






class BoardJoinView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        board_id = request.POST.get('board_id')
        board = Board.objects.get(id=board_id)

        if board.author != request.user:
            return HttpResponseForbidden("Только создатель доски может добавить участника.")

        user_id = request.POST.get('user_select')
        user = get_user_model().objects.get(id=user_id)
        board.users.add(user)

        return redirect('list_column', pk=board_id)


class BoardIndexView(LoginRequiredMixin, ListView):
    model = Board
    template_name = 'board/index.html'
    context_object_name = 'boards'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context
    
    def index(request):
        return render(request, 'base.html')
    


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

    def create(request):
        return render(request, 'board/create_boeard.html')

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

    def update(request):
        return render(request, 'board/update_board.html')

class BoardDeleteView(PermissionRequiredMixin, DeleteView):
    model = Board
    template_name = 'board/delete_board.html'
    context_object_name = 'boards'
    success_url = reverse_lazy('index')
    permission_required = 'project.delete_board'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user


    def delete(request):
        return render(request, 'board/delete.html')
