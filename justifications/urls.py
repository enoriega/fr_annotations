from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^annotate/(?P<id>[0-9]+)/?$', views.annotate_one, name='annotate_one'),
    url(r'^annotate/?$', views.annotate, name='annotate'),
    url(r'^skipped/?$', views.skipped, name='skipped'),
    url(r'^save/?$', views.save_annotation, name="save")
]
