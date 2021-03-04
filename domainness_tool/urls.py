from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('verify_domain_tool', views.verify_domain_tool, name='verify_domain_tool'),
    path(r'add_entry_domain_tool/', views.add_entry_domain_tool, name='add_entry_domain_tool'),
]