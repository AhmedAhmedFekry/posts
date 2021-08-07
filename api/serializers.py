from rest_framework import serializers
from core.models import Post, Comment, Category, Like

from django.contrib.auth.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        user_details = dict()
        user_details["id"] = instance.id
        user_details["email"] = instance.email
        user_details["name"] = instance.username
 
   
        return user_details
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    # create_by = CurrentUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommenttSerializer(serializers.ModelSerializer):
    # commenter = CurrentUserSerializer(read_only=True)
    # post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'post', 'commenter', 'like']
        depth = 1


class LikeSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(read_only=True)
    comment = CommenttSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
