
from django.urls import path
from core import views
from accounts import views as acviews
from core.views import tagged

urlpatterns = [
    path('', views.show_posts, name='home'),
    path('tag/<slug:slug>/', tagged, name="tagged"),
    path('add-post/', views.add_post, name='add_post'),
    path('category/<slug:slug_category>',
         views.category_posts, name='category_post'),
    path('category/<slug:slug_category>/<slug:slug_post>/',
         views.show_post_detail, name='post_detail'),
    path('<int:num_post>/add-comment', views.add_comment, name='add_comment'),
    #     path('<int:num_post>/add-like/<int:num_comment>',
    #          views.addlike, name='like_comment'),
    path('addlike/<int:num_post>/<int:num_comment>',
         views.addlike, name='addlike'),
    path('delete-comment/<int:num_post>/<int:num_comment>',
         views.delete_comment, name='delete_comment'),
    # path('<int:num_board>/<int:num_topic>', views.topics_posts, name='posts'),
    path('profile/', acviews.show_profile, name='profile'),
    path('profile/update/', acviews.user_update, name='user_update'),
    path('favorite-comments/', views.favorite, name='favorite_comments'),




]
