from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='my-profile'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('follow/<str:username>/', views.FollowView.as_view(), name='follow'),
    path('suggested/', views.SuggestedUsersView.as_view(), name='suggested'),
]
