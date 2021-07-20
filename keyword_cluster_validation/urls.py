from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cluster_validation', views.cluster_validation, name='cluster_validation'),
]