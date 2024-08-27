from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
from . import models

# Create your views here.

def home(request):
    return render(request,'home.html')

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
                return redirect(home)

        else:
            messages.error(request, 'Invalid credentials.')
    return render(request,'login.html')

def accessInfo(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')

        current_user = get_object_or_404(models.CustomUser, pk=request.user.id)
        print(f'\n\n{current_user}')
        print(f'\n\n{current_user.DeptId}')
        status_current_user = current_user.status
        if current_user.status == 'SO':
            current_user.status = 'Store Officer'
        elif current_user.status == 'PO':
            current_user.status = 'Procurement Officer'
        elif current_user.status == 'FO':
            current_user.status = 'Finance Officer'
        else:
            current_user.status = 'None'
        
        Dept_name = current_user.DeptId

        # check if user has given a new input or gave the previous input 
        if current_user.username == new_username and current_user.first_name == new_first_name and current_user.last_name == new_last_name and current_user.email == new_email:
            messages.success(request, 'No changes to made.')
            return render(request, 'showInfo.html', {'logined_user_info': current_user, 'Dept_name': Dept_name})

        # chk if username or email is unique or duplicate
        # if user has not changed the username, then it will be excluded and filtered results will contain objects that matched with the new entered username.
        if models.CustomUser.objects.filter(username = new_username).exclude(username = request.user.username):
            messages.error(request, 'username already exists.')
            return render(request, 'showInfo.html', {'logined_user_info': current_user, 'Dept_name': Dept_name})
        elif models.CustomUser.objects.filter(email = new_email).exclude(email = request.user.email):
            messages.error(request, 'Email already exists.')
            return render(request, 'showInfo.html', {'logined_user_info': current_user, 'Dept_name': Dept_name})

        # saving changes

        # status_to_be_displayed: store the status in the format that is to be rendered on html page (i.e store officer) 
        status_to_be_displayed = current_user.status
        current_user.username = new_username
        current_user.first_name = new_first_name
        current_user.last_name = new_last_name
        current_user.email = new_email

        # status_current_user: store the status in the format that is used in db (i.e SO)
        current_user.status = status_current_user
        current_user.save()
        messages.success(request, 'Your changes has been saved.')
        current_user.status = status_to_be_displayed
        return render(request, 'showInfo.html', {'logined_user_info': current_user, 'Dept_name': Dept_name})

    logined_user_info = {
        'username': '',
        'id': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'status': '',
        'DeptId_id': ''
    }
    user = models.CustomUser.objects.filter(username=request.user.username)
    user_info = user.values()
    user_info = user_info[0]
    for attr in logined_user_info:
        logined_user_info[attr] = user_info[attr]
    
    # get dept name 
    Dept_name = models.Department.objects.get(pk=logined_user_info['DeptId_id'])

    # replace status pnemonics with full forms
    if logined_user_info['status'] == 'SO':
         logined_user_info['status'] = 'Store Officer'
    elif logined_user_info['status'] == 'PO':
         logined_user_info['status'] = 'Procurement Officer'
    elif logined_user_info['status'] == 'FO':
         logined_user_info['status'] = 'Finance Officer'
    else:
         logined_user_info['status'] = 'None'

    return render(request,'showInfo.html', {'logined_user_info': logined_user_info, 'Dept_name': Dept_name})