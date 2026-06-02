"""
conectio_project URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from posts.views import FeedView, SearchView, ExploreView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App endpoints
    path('api/users/', include('users.urls')),
    path('api/posts/', include('posts.urls')),

    # Feed, Search, Explore (top-level API routes)
    path('api/feed/', FeedView.as_view(), name='feed'),
    path('api/search/', SearchView.as_view(), name='search'),
    path('api/explore/', ExploreView.as_view(), name='explore'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
