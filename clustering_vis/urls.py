from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('visualization', views.visualization, name='visualization'),
    path(r'iteration_input/', views.iteration_input, name='iteration_input'),
]