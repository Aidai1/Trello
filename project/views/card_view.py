from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from project.models import Card, Column, Checklist, ChecklistItem
from project.forms import CardForm


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "cards/create_card.html"
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
    permission_required = 'project.delete_card'
