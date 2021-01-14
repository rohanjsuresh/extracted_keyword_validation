from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('keyword_pages/<str:keyword>', views.dynamic_lookup_view, name='dynamic_lookup_view'),
    path('keyword_pages', views.keyword_pages, name='keyword_pages'),
    path('verify_relationship_tool', views.verify_relationship_tool, name='verify_relationship_tool'),
    path(r'search/', views.search, name='search'),
]