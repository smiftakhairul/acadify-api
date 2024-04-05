from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='api.register'),
    path('login/', views.login, name='api.login'),
    # path('update-user-profile/', views.user_profile, name='update-user-profile'),
    # path('user-profile/<int:user_id>/', views.get_user_profile, name='user-profile'),
]
