from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add$', views.add),
    url(r'^(?P<user_id>\d+)$', views.show), 
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite), 
    url(r'^unfavorite/(?P<quote_id>\d+)$', views.unfavorite), 
    
    
]