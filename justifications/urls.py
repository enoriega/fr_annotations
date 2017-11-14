from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^annotate/?$', views.annotate, name='annotate'),
    url(r'^save/?$', views.save_annotation, name="save")
]
