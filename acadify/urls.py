from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('acadify.api.urls')),
]
