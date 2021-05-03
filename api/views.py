from django.shortcuts import render
from django.utils.text import slugify
from core.models import Post, Category, Comment, Like
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, CommenttSerializer, LikeSerializer, CurrentUserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        c = Category.objects.all()
        return c
# Search _ Filtering Data Inside ModelViewset

    # def retrieve(self, request, *args, **kwargs):
    #     params = kwargs
    #     print(params)
    #     p = params['pk']

    #     cate = Category.objects.filter(title=p)
    #     serializer = CategorySerializer(cate, many=True)
    #     return Response(serializer.data)

    #  Search in GET _Model Filtering With 2 Parameters Or More
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params)
        plist = params['pk'].split('-')
        cate = Category.objects.filter(title=plist[0], id=int(plist[1]))
        serializer = CategorySerializer(cate, many=True)
        return Response(serializer.data)
# Override Create Action _ CREATE Method ModelViewSet

    def create(self, request, *args, **kwargs):
        ca_data = request.data
        print('category data', ca_data)
        newCategory = Category.objects.create(
            title=ca_data["title"], status=ca_data['status'], slug=slugify(ca_data['title']))
        newCategory.save()
        serialize = CategorySerializer(newCategory)
        print('created is done')
        return Response(serialize.data)


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
    print(request.query_params)
    print(request.query_params['id'])
    result = int(request.query_params['id']) * 3

    return Response({'message': 'we are recive respone test', 'result': result})
