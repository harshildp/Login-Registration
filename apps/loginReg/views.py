from django.shortcuts import render, redirect
from .models import *
from django.contrib.messages import error

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Renders ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def index(req):
    return render(req, 'loginReg/index.html')

def home(req):
    if 'user_id' not in req.session:
        return redirect('/')

    print req.session['user_id']
    
    return render(req, 'loginReg/home.html')

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~ Processes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def login(req):
    user = User.objects.login(req.POST)
    if user:
        req.session['user_id'] = user.id
        print req.session['user_id']
        return redirect('/home')
    
    error(req, 'Invalid email or password')
    return redirect('/')

def register(req):
    errors = User.objects.validate(req.POST)
    if len(errors):
        for key, message in errors.iteritems():
            error(req, message, extra_tags=key)
        return redirect('/')
    else:
        user = User.objects.createUser(req.POST)
        req.session['user_id'] = user.id
        return redirect('/home')
    
def logoff(req):
    req.session.clear()
    return redirect('/')
