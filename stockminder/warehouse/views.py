from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . import models

# Create your views here.

def loginform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            user = models.CustomUser.objects.filter(username=username)
            user_info = user.values()
            user = user[0] # filter returns a list having a dict at 0 index, the dict have all attrs of search object.
            if user_info[0]['status'] == 'NA':
                messages.error(request, 'You are not an authorized user.')
            else:
                login(request, user)
                return render(request,'home.html')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request,'login.html')