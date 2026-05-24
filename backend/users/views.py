from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile, Connection
from .serializers import ProfileSerializer, RegisterSerializer, UserMinimalSerializer


class RegisterView(generics.CreateAPIView):
    """Register a new user account."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'Account created successfully.',
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the authenticated user's profile."""
    serializer_class = ProfileSerializer

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileDetailView(generics.RetrieveAPIView):
    """Get any user's profile by username."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    queryset = Profile.objects.select_related('user')


class FollowView(APIView):
    """Follow or unfollow a user."""

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        connection, created = Connection.objects.get_or_create(
            follower=request.user,
            following=target_user,
        )

        if not created:
            connection.delete()
            return Response({'status': 'unfollowed', 'username': username})

        return Response({'status': 'followed', 'username': username}, status=status.HTTP_201_CREATED)


class SuggestedUsersView(generics.ListAPIView):
    """Get suggested users to follow."""
    serializer_class = UserMinimalSerializer

    def get_queryset(self):
        following_ids = self.request.user.following.values_list('following_id', flat=True)
        return User.objects.exclude(
            id__in=list(following_ids) + [self.request.user.id]
        ).select_related('profile')[:10]
