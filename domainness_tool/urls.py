from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('verify_domain_tool', views.verify_domain_tool, name='verify_domain_tool'),
    path('verify_domain_tool/<str:keyword>', views.verify_domain_tool_iframe, name='verify_domain_tool_iframe'),
    path(r'add_entry_domain_tool/', views.add_entry_domain_tool, name='add_entry_domain_tool'),
]