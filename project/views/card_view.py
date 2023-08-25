from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from project.models import Card, Column, Checklist
from project.forms import CardForm


class CardCreateView(CreateView):
    model = Card
    template_name = "cards/create_card.html"
    context_object_name = "cards"
    form_class = CardForm

    def get_success_url(self):
        return reverse('detail_column_cards', kwargs={'pk': self.kwargs.get('pk')})




class CardDetailView(DetailView):
    model = Card
    template_name = 'cards/detail_card.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = self.object
        comments = card.comments.order_by('-created_at')
        context['comments'] = comments
        checklists = Checklist.objects.filter(card=card)
        context['checklists'] = checklists
        return context


class CardUpdateView(UpdateView):
    model = Card
    template_name = 'cards/update_card.html'
    success_url = reverse_lazy('index')



class CardDeleteView(DeleteView):
    model = Card
    template_name = 'cards/delete_card.html'
    success_url = reverse_lazy('index')
    permission_required = 'project.delete_card'
