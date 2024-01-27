from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        myuser = auth.authenticate(username=username, password=password)

        if myuser and myuser.is_superuser:
            request.session['username'] = username
            auth_login(request, myuser)
            authors = reverse('Authors')
            return redirect(authors)
        else:
            messages.info(request, "Invalid username or password")
            return redirect('Login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('Login')
    

    
