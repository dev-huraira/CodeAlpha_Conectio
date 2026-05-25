from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Connection
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserPublicSerializer,
    UserPrivateSerializer,
    UserMinimalSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/users/register/ — Create account, return JWT tokens + user data."""
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        user_data = UserPublicSerializer(user, context={'request': request}).data

        return Response(
            {
                'user': user_data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'message': 'Account created successfully.',
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/users/login/ — Authenticate with email + password, return JWT."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Look up user by email
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'No account found with this email.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check password
        if not user.check_password(password):
            return Response(
                {'detail': 'Incorrect password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        user_data = UserPublicSerializer(user, context={'request': request}).data

        return Response({
            'user': user_data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
        })


class LogoutView(APIView):
    """POST /api/users/logout/ — Blacklist the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'detail': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'detail': 'Successfully logged out.'},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MeView(generics.RetrieveAPIView):
    """GET /api/users/me/ — Return the authenticated user's full profile."""
    serializer_class = UserPrivateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileDetailView(generics.RetrieveAPIView):
    """GET /api/users/profile/<username>/ — View any user's public profile."""
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'
    queryset = User.objects.all()


class FollowView(APIView):
    """POST /api/users/follow/<username>/ — Follow or unfollow a user."""

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if target_user == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connection, created = Connection.objects.get_or_create(
            follower=request.user,
            following=target_user,
        )

        if not created:
            connection.delete()
            return Response({'status': 'unfollowed', 'username': username})

        return Response(
            {'status': 'followed', 'username': username},
            status=status.HTTP_201_CREATED,
        )


class SuggestedUsersView(generics.ListAPIView):
    """GET /api/users/suggested/ — Users you might want to follow."""
    serializer_class = UserMinimalSerializer

    def get_queryset(self):
        following_ids = self.request.user.following_set.values_list(
            'following_id', flat=True
        )
        return User.objects.exclude(
            id__in=list(following_ids) + [self.request.user.id]
        )[:10]
