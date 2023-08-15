from django.urls import path
from .views import recently_viewed_boards, activate, signup, AddToFavoritesView
from django.contrib.auth.views import LoginView, LogoutView
from project.views import UserDetailView


urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', signup, name='signup'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail_account'),
    path('board/add_to_favorites/', AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('recently_viewed_boards/', recently_viewed_boards, name='recently_viewed_boards'),
]