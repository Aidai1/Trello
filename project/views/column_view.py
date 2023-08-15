from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from project.models import Column, Board
from project.forms import ColumnForm


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
