from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from project.models import Board
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views import View


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


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


class UserDetailView(UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def post(self, request, *args, **kwargs):
        board = self.get_object()
        request.user.add_to_favorites(board)
        return HttpResponseRedirect(self.request.path)

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        return user == self.request.user



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


@login_required
def recently_viewed_boards(request):
    user_profile = User.objects.get(pk=request.user.id)
    recently_viewed_boards = user_profile.recently_viewed_boards.all().order_by('-id')[:6]
    return render(request, 'recently_viewed_boards.html', {'recently_viewed_boards': recently_viewed_boards})