from django.shortcuts import render, redirect
from .models import *
from ..loginReg.models import * 
from django.contrib.messages import error

#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Renders ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    quotes = Quote.objects.get_favorites(request.session['user_id'])
    data = {
        'favorites': quotes[0],
        'other': quotes[1]
    }
    return render(request, 'quotes/home.html', data)

def show(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    posted = Quote.objects.get_posted(user_id)
    data = {
        'user':posted[0],
        'posted': posted[1],
        'count':posted[2]
    }
    return render(request, 'quotes/show.html', data)
#=================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~ Processes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================================

def add(request):
    errors = Quote.objects.validate(request.POST)
    if len(errors):
        for key, message in errors.iteritems():
            error(request, message, extra_tags=key)
    else:
        Quote.objects.add_quote(request.POST, request.session['user_id'])

    return redirect('/quotes')

def favorite(request, quote_id):
    Quote.objects.favorite(quote_id, request.session['user_id'])
    return redirect('/quotes')

def unfavorite(request, quote_id):
    Quote.objects.unfavorite(quote_id, request.session['user_id'])
    return redirect('/quotes')