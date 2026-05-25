from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.MeView.as_view(), name='me'),
    path('me/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('me/avatar/', views.AvatarUploadView.as_view(), name='avatar-upload'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('follow/<str:username>/', views.FollowView.as_view(), name='follow'),
    path('suggested/', views.SuggestedUsersView.as_view(), name='suggested'),
    # Direct username lookup (used by frontend profile page)
    path('<str:username>/', views.ProfileDetailView.as_view(), name='user-profile'),
]
