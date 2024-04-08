from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # user
    path('user/', views.user, name='user'),
    path('user/update/', views.update_user, name='user.update'),
    path('user/<int:pk>/', views.show_user, name='user.show'),
    # post
    path('posts/', views.list_posts, name='posts.list'),
    path('posts/create/', views.create_post, name='posts.create'),
    path('posts/<int:pk>/update/', views.update_post, name='posts.update'),
    path('posts/<int:pk>/', views.show_post, name='posts.show'),
    path('posts/<int:pk>/delete/', views.delete_post, name='posts.delete'),
    # like
    path('like/', views.like, name='like'),
    # comment
    path('comments/create/', views.create_comment, name='comments.create'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='comments.delete'),
]
