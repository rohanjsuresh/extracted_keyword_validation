"""extracted_keyword_validation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url



urlpatterns = [
    path(r'', include('keyword_relation.urls')),
    path(r'domainness_tool/', include('domainness_tool.urls')),
    path(r'definition_tool/', include('definition_tool.urls')),
    path(r'clustering_vis/', include('clustering_vis.urls')),
    path(r'cluster_validation/', include('keyword_cluster_validation.urls')),
    path('admin/', admin.site.urls),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path(r"users/", include('users.urls')),
    path(r"myadmin/", include('admin_extended.urls')),
]
