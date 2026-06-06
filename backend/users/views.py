from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from .models import Connection
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserPublicSerializer,
    UserPrivateSerializer,
    UserMinimalSerializer,
    UserFollowSerializer,
    UpdateProfileSerializer,
    AvatarUploadSerializer,
    BannerUploadSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/users/register/ — Create account, return JWT tokens + user data."""
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
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

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
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

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        profile_user = self.get_object()
        if request.user.is_authenticated:
            response.data['is_following_them'] = Connection.objects.filter(
                follower=request.user, following=profile_user
            ).exists()
        else:
            response.data['is_following_them'] = False
        return response


class FollowView(APIView):
    """POST /api/users/follow/<username>/ — Follow or unfollow a user."""
    permission_classes = [permissions.IsAuthenticated]

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

        existing = Connection.objects.filter(
            follower=request.user, following=target_user
        ).first()

        if existing:
            existing.delete()
            # Recompute actual counts from the Connection table
            target_user.followers_count = Connection.objects.filter(following=target_user).count()
            target_user.save(update_fields=['followers_count'])
            request.user.following_count = Connection.objects.filter(follower=request.user).count()
            request.user.save(update_fields=['following_count'])
            return Response({
                'is_following': False,
                'followers_count': target_user.followers_count,
            })

        Connection.objects.create(follower=request.user, following=target_user)
        # Recompute actual counts from the Connection table
        target_user.followers_count = Connection.objects.filter(following=target_user).count()
        target_user.save(update_fields=['followers_count'])
        request.user.following_count = Connection.objects.filter(follower=request.user).count()
        request.user.save(update_fields=['following_count'])
        return Response({
            'is_following': True,
            'followers_count': target_user.followers_count,
        }, status=status.HTTP_201_CREATED)


class SuggestedUsersView(generics.ListAPIView):
    """GET /api/users/suggested/ — Users you might want to follow."""
    serializer_class = UserMinimalSerializer
    pagination_class = None

    def get_queryset(self):
        following_ids = self.request.user.following_set.values_list(
            'following_id', flat=True
        )
        return User.objects.exclude(
            id__in=list(following_ids) + [self.request.user.id]
        ).order_by('?')[:5]


class UpdateProfileView(APIView):
    """PATCH /api/users/me/update/ — Update own profile fields."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = UpdateProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return updated full profile
        profile_data = UserPrivateSerializer(
            request.user, context={'request': request}
        ).data
        return Response(profile_data)


class AvatarUploadView(APIView):
    """POST /api/users/me/avatar/ — Upload avatar image."""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        avatar_file = serializer.validated_data['avatar']
        user = request.user
        # Delete old avatar file if exists
        if user.avatar:
            user.avatar.delete(save=False)
        user.avatar = avatar_file
        user.save(update_fields=['avatar'])

        avatar_url = request.build_absolute_uri(user.avatar.url)
        return Response({
            'avatar': avatar_url,
            'message': 'Avatar uploaded successfully.',
        })


class BannerUploadView(APIView):
    """PATCH /api/users/me/banner/ — Upload banner image."""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        serializer = BannerUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        banner_file = serializer.validated_data['banner']
        user = request.user
        # Delete old banner file if exists
        if user.banner:
            user.banner.delete(save=False)
        user.banner = banner_file
        user.save(update_fields=['banner'])

        banner_url = request.build_absolute_uri(user.banner.url)
        return Response({
            'banner': banner_url,
            'message': 'Banner uploaded successfully.',
        })


class FollowersListView(generics.ListAPIView):
    """GET /api/users/<username>/followers/ — List of a user's followers."""
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        return User.objects.filter(
            following_set__following__username=username
        )


class FollowingListView(generics.ListAPIView):
    """GET /api/users/<username>/following/ — List of users someone follows."""
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        return User.objects.filter(
            followers_set__follower__username=username
        )
