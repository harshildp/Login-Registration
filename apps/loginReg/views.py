from django.shortcuts import render, redirect
from .models import *
from django.contrib.messages import error

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Renders ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def index(request):
    return render(request, 'loginReg/index.html')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')

    print request.session['user_id']
    
    return render(request, 'loginReg/home.html')

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~ Processes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def login(request):
    user = User.objects.login(request.POST)
    if user:
        request.session['user_id'] = user.id
        print request.session['user_id']
        return redirect('/home')
    
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
        return redirect('/home')
    
def logoff(request):
    request.session.clear()
    return redirect('/')
