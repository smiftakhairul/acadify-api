from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('register/', views.register, name='api.register'),
    path('login/', views.login, name='api.login'),
    path('logout/', views.logout, name='api.logout'),
    # user
    path('user/', views.user, name='api.user'),
    path('user/update/', views.update_user, name='api.user.update'),
    # post
    path('posts/', views.list_posts, name='api.posts.list'),
    path('posts/create/', views.create_post, name='api.posts.create'),
    path('posts/<int:pk>/update/', views.update_post, name='api.posts.update'),
    path('posts/<int:pk>/', views.show_post, name='api.posts.show'),
    path('posts/<int:pk>/delete', views.delete_post, name='api.posts.delete'),
]
