from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from project.models import Card, Checklist, ChecklistItem
from django.contrib.auth.mixins import PermissionRequiredMixin
from project.forms import ChecklistForm, ChecklistItemForm


class ChecklistCreateView(CreateView):
    model = Checklist
    template_name = 'checklist/checklist_create.html'
    form_class = ChecklistForm

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk})

    def form_valid(self, form):
        card = get_object_or_404(Card, pk=self.kwargs.get('pk'))
        form.instance.card = card
        return super().form_valid(form)


class ChecklistUpdateView(PermissionRequiredMixin, UpdateView):
    model = Checklist
    template_name = 'checklist/checklist_update.html'
    form_class = ChecklistForm
    context_object_name = 'checklists'

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk})

    def has_permission(self):
        return self.request.user.has_perm('project.change_checklist') or self.get_object().author == self.request.user


class ChecklistDeleteView(UserPassesTestMixin, DeleteView):
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