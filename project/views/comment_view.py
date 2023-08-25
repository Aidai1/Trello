from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from project.forms import CommentForm
from project.models import Comment, Card


class CommentCreateView(CreateView):
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


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.has_perm('project.delete_comment') or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('detail_card', kwargs={'pk': self.object.card.pk })