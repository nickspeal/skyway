from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^go', views.go, name='go'),
    url(r'^coordinates',views.coordinates, name='coordinates'),
    url(r'^homecoordinates',views.homecoordinates, name='homecoordinates'),
    url(r'^connect',views.connect, name='connect')

]