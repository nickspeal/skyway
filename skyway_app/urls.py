from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^go', views.go, name='go'),
    url(r'^rtl', views.rtl, name='rtl'),
    url(r'^coordinates',views.coordinates, name='coordinates')
]