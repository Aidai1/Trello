from django.urls import path, include
from . import views
from .views import user_detail, create

app_name = 'project'

urlpatterns = [
   path('user_detail/', user_detail, name='user_detail'),
   path('create/', create, name='create')
]

