from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer

User = get_user_model()


class PostListCreateView(generics.ListCreateAPIView):
    """List all posts (feed) or create a new post."""

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related('author').all()
        # Filter by author username if provided
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Increment posts_count on user
        self.request.user.posts_count = (self.request.user.posts_count or 0) + 1
        self.request.user.save(update_fields=['posts_count'])

    def create(self, request, *args, **kwargs):
        """Override to return full post data with author after creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Re-serialize with PostSerializer to include author, time_ago, etc.
        post = Post.objects.select_related('author').get(pk=serializer.instance.pk)
        output = PostSerializer(post, context={'request': request})
        return Response(output.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class PostDetailView(generics.RetrieveDestroyAPIView):
    """Get or delete a single post."""
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('author')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only delete your own posts.')
        # Decrement posts_count on user
        user = instance.author
        user.posts_count = max(0, (user.posts_count or 0) - 1)
        user.save(update_fields=['posts_count'])
        instance.delete()


class LikeView(APIView):
    """Like or unlike a post."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save(update_fields=['likes_count'])
            return Response({'status': 'unliked', 'likes_count': post.likes_count})

        post.likes_count = post.likes_count + 1
        post.save(update_fields=['likes_count'])
        return Response(
            {'status': 'liked', 'likes_count': post.likes_count},
            status=status.HTTP_201_CREATED,
        )


class CommentListCreateView(generics.ListCreateAPIView):
    """List comments on a post or add a new comment."""
    serializer_class = CommentSerializer
    pagination_class = None  # Return all comments without pagination

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['pk']
        ).select_related('author')

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)
        # Increment comments_count
        post.comments_count = post.comments_count + 1
        post.save(update_fields=['comments_count'])

    def create(self, request, *args, **kwargs):
        """Override to return full comment with author after creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Re-serialize with full author details
        comment = Comment.objects.select_related('author').get(pk=serializer.instance.pk)
        output = CommentSerializer(comment, context={'request': request})
        return Response(output.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class CommentDeleteView(generics.DestroyAPIView):
    """Delete a comment. Only the comment author can delete."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['pk']
        ).select_related('author')

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only delete your own comments.')
        post = instance.post
        instance.delete()
        # Decrement comments_count
        post.comments_count = max(0, post.comments_count - 1)
        post.save(update_fields=['comments_count'])


class UserPostsView(generics.ListAPIView):
    """List all posts by a specific user."""
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.filter(
            author__username=self.kwargs['username']
        ).select_related('author')
