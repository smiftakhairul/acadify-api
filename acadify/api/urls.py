from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='api.register'),
    path('login/', views.login, name='api.login'),
    path('logout/', views.logout, name='api.logout'),
    path('user/', views.user, name='api.user'),
    path('user/update/', views.update_user, name='api.user.update'),
]
