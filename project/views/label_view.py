from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView
from project.models import Card, Label
from project.forms import CardLabelForm


class CardLabelCreateView(CreateView):
    model = Label
    form_class = CardLabelForm
    template_name = 'label/label_create.html'

    def form_valid(self, form):
        card_id = self.kwargs['pk']
        card = get_object_or_404(Card, id=card_id)
        color = form.cleaned_data['color']
        label = Label.objects.create(name=form.cleaned_data['name'], color=color)
        card.labels.add(label)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_id = self.kwargs['pk']
        card = get_object_or_404(Card, id=card_id)
        context['card'] = card
        return context

    def get_success_url(self):
        card_id = self.kwargs['pk']
        return reverse('detail_card', kwargs={'pk': card_id})
