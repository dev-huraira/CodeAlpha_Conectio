from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/like/', views.LikeView.as_view(), name='post-like'),
    path('<int:pk>/comments/', views.CommentListCreateView.as_view(), name='post-comments'),
    path('user/<str:username>/', views.UserPostsView.as_view(), name='user-posts'),
]
