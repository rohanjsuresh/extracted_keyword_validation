from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_tool', views.admin_tool, name='admin_tool'),
    path('populate-chart/', views.populate_chart, name='populate-chart'),
    path('simple_upload/', views.simple_upload, name='simple_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
