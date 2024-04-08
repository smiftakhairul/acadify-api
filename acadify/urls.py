from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = []

if settings.ADMIN_ENABLED:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(('acadify.api.urls', 'api'), namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
