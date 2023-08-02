from django.shortcuts import render



def index(request):
    return render(request, 'project/index.html')

def user_detail(request):
    return render (request, 'user/user_detail')
   
  
def active_email(request):
    return render(request, 'user/active_email.html')


def create(request):
    return render(request, 'boards/create_board.html')


def delete(request):
    return render(request, 'boards/delete.html')

def update(request):
    return render(request, 'boards/update_board.html')


   