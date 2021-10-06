from django.urls import path
from .views import (
    #PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    #UserPostListView,

    HabitListView,
    HabitDetailView,
    UserHabitListView,
    HabitCreateView,
    HabitUpdateView,
    HabitDeleteView)
from . import views

urlpatterns = [
    path('', HabitListView.as_view(), name='blog-home'),
    path('habit/<int:pk>', HabitDetailView.as_view(), name='detail-habit'),
    path('user/<str:username>', UserHabitListView.as_view(), name='user-habits'),
    path('habit/new', HabitCreateView.as_view(), name='create-habit'),
    path('habit/<int:pk>/update/', HabitUpdateView.as_view(), name='update-habit'),
    path('habit/<int:pk>/delete/', HabitDeleteView.as_view(), name='delete-habit'),

    
    path('habit/<int:pk>/create_post/', PostCreateView.as_view(), name='create-post'),

    path('habit/<int:pk>/post/', PostDetailView.as_view(), name='detail-post'),
    
    path('habit/post/<int:pk>/update/', PostUpdateView.as_view(), name='update-post'),
    path('habit/post/<int:pk>/delete', PostDeleteView.as_view(), name='delete-post'),
    path('about/', views.about, name='blog-about'),
]