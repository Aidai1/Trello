from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from project.models import Board
from project.forms import BoardForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views import View




class BoardIndexView(ListView):
    model = Board
    template_name = 'board/index.html'
    context_object_name = 'boards'

  
    def index(request):
        return render(request, 'base.html')
    


class BoardCreateView(CreateView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board/create_board.html'
    form_class = BoardForm
    

    def form_valid(self, form):
        board = form.save(commit=False)
        board.author = self.request.user
        board.save()
        board.users.set(form.cleaned_data['users'])
        return super().form_valid(form)

    def create(request):
        return render(request, 'board/create_board.html')

class BoardDetailView(DetailView):
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
    permission_required = 'project.update_view'


    def update(request):
        return render(request, 'board/update_board.html')

class BoardDeleteView(DeleteView):
    model = Board
    template_name = 'board/delete_board.html'
    context_object_name = 'boards'
    permission_required = 'project.delete_board'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user


    def delete(request):
        return render(request, 'board/delete.html')
