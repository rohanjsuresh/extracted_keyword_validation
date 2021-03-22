from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('verify_definition_tool', views.verify_definition_tool, name='verify_definition_tool'),
    path(r'add_entry_definition_tool/', views.add_entry_definition_tool, name='add_entry_definition_tool'),
]