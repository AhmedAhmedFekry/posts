from django.shortcuts import render
from core.models import Post, Category, Comment, Like
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, CommenttSerializer, LikeSerializer, CurrentUserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
#################  api   ###########################


class Viewsets_Post(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        # check all fields is valid before attempting to save
        serializer.is_valid(raise_exception=True)
        serializer.save(create_by=request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['POST', 'GET'])
    def comments(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.method == 'GET':
            self.serializer_class = CommenttSerializer
            queryset = Comment.objects.filter(post=post)
            serializer = CommenttSerializer(
                queryset, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            self.serializer_class = CommenttSerializer
            queryset = Comment.objects.filter(post=post)
            serializer = CommenttSerializer(
                data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(commenter=request.user, post=post)
            return Response(serializer.data)

    @action(detail=False, methods=['DELETE'])
    def remove_comment(self, request, pk, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        queryset = Comment.objects.filter(pk=comment_id)
        serializer = CommenttSerializer(
            data=request.data, context={'request': request})
        if comment.delete():
            return Response({'message': 'Comment deleted'})
        else:
            return Response({'message': 'unable to delete comment'})


class Viewsets_Category(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Viewsets_Comment(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommenttSerializer


class Viewsets_Like(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer


@api_view()
@permission_classes([AllowAny])
def firstfunc(request):
    return Response({'message': 'we are recive respone test'})
