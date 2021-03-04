from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('keyword_pages/<str:keyword>', views.dynamic_lookup_view, name='dynamic_lookup_view'),
    path('keyword_pages', views.keyword_pages, name='keyword_pages'),
    path('verify_relationship_tool', views.verify_relationship_tool, name='verify_relationship_tool'),
    path(r'search/', views.search, name='search'),
    # path(r'add_entry/', views.add_entry, name='add_entry'),
    path(r'add_entry_rel_tool/', views.add_entry_rel_tool, name='add_entry_rel_tool'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)