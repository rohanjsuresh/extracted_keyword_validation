from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    path('keyword_pages_search/<str:keyword>', views.dynamic_lookup_view, name='dynamic_lookup_view'),
    # path('keyword_pages_default', views.keyword_pages_default, name='keyword_pages_default'),
    # path('keyword_pages/<str:page_num>', views.keyword_pages, name='keyword_pages'),
    path('keyword_pages', views.keyword_pages, name='keyword_pages'),
    path('verify_relationship_tool', views.verify_relationship_tool, name='verify_relationship_tool'),
    path('find_similar_keyword_default', views.find_similar_keyword_default, name='find_similar_keyword_default'),
    path(r'search/', views.search, name='search'),
    path(r'search_similar/', views.search_similar, name='search_similar'),
    path(r'search_similar_result/', views.search_similar_result, name='search_similar_result'),
    path(r'add_entry/', views.add_entry, name='add_entry'),
    path(r'add_entry_rel_tool/', views.add_entry_rel_tool, name='add_entry_rel_tool'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)