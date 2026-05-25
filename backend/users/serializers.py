from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Registration serializer — validates and creates a new user."""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2',
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password2': 'Passwords do not match.'}
            )
        return data

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.'
            )
        return value.lower()

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Login serializer — accepts email + password."""
    email = serializers.EmailField()
    password = serializers.CharField()


class UserPublicSerializer(serializers.ModelSerializer):
    """Public profile — safe to expose to any authenticated user."""
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'bio', 'avatar', 'headline',
            'followers_count', 'following_count', 'posts_count',
            'date_joined',
        ]
        read_only_fields = fields


class UserPrivateSerializer(UserPublicSerializer):
    """Private profile — includes website, only for own profile."""

    class Meta(UserPublicSerializer.Meta):
        fields = UserPublicSerializer.Meta.fields + ['website']
        read_only_fields = fields


class UserMinimalSerializer(serializers.ModelSerializer):
    """Lightweight serializer for embedding in other responses (posts, comments)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'headline']


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile fields."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'headline', 'website']

    def validate_bio(self, value):
        if len(value) > 300:
            raise serializers.ValidationError('Bio must be 300 characters or fewer.')
        return value

    def validate_headline(self, value):
        if len(value) > 120:
            raise serializers.ValidationError('Headline must be 120 characters or fewer.')
        return value


class AvatarUploadSerializer(serializers.Serializer):
    """Serializer for avatar file upload validation."""
    avatar = serializers.ImageField()

    def validate_avatar(self, value):
        # Max 5MB
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Avatar file size must be under 5MB.')
        return value
