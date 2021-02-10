from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login', views.login),
    url(r'^register', views.register),
    url(r'^signin', views.signin),
    url(r'^create', views.create),
    url(r'^success', views.success),
    url(r'^thewall', views.show),
    url(r'^logout', views.logout),
    url(r'^logoutofthewall', views.logoutofthewall),
    url(r'^message', views.message),
    url(r'^comment', views.comment),
    url(r'^delete', views.delete),
    url(r'^remove', views.remove),
]