
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import Viewsets_Post, Viewsets_Like, Viewsets_Category, Viewsets_Comment, CurrentUserViewSet, firstfunc
router = DefaultRouter()
router.register('users', CurrentUserViewSet)
router.register('posts', Viewsets_Post)
router.register('categories', Viewsets_Category, basename='categories')
router.register('comments', Viewsets_Comment)
router.register('likes', Viewsets_Like)
urlpatterns = [
    path('viewsets/', include(router.urls)),
    path('posts/<pk>/addcomment/',
         Viewsets_Post.as_view({'get': 'comments', 'post': 'comments'})),
    path('posts/<pk>/comment/<int:comment_id>',
         Viewsets_Post.as_view({'delete': 'remove_comment'})),

    path('testfunc/', firstfunc)

    #  path('posts/<pk>/comment/<int:comment_id>/update',
    #          Viewsets_Post.as_view({'put': 'remove_comment'}))
]
