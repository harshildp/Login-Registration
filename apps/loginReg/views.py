from django.shortcuts import render, redirect
from .models import *
from django.contrib.messages import error

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Renders ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def index(request):
    if 'user_id' in request.session:
        return redirect('/quotes')
    return render(request, 'loginReg/index.html')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    return render(request, 'loginReg/home.html')

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~ Processes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def login(request):
    user = User.objects.login(request.POST)
    if user:
        request.session['user_id'] = user.id
        request.session['name'] = user.first_name
        return redirect('/quotes')
    
    error(request, 'Invalid email or password')
    return redirect('/')

def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors):
        for key, message in errors.iteritems():
            error(request, message, extra_tags=key)
        return redirect('/')
    else:
        user = User.objects.createUser(request.POST)
        request.session['user_id'] = user.id
        request.session['name'] = user.first_name        
        return redirect('/quotes')
    
def logoff(request):
    request.session.clear()
    return redirect('/')
