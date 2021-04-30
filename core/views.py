from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Comment, Category
from core.forms import PostForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from core.models import Like
from django.utils.text import slugify
from accounts.models import UserProfile
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator


def show_posts(request):
    categories = Category.objects.filter(status="True")

    posts = Post.objects.all().order_by('-id')
    common_tags = Post.tags.most_common()[:10]

    lastpost = Post.objects.all().order_by('-id')[:3]
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    print(type(page_number))
    if page_number == None:
        page_number = '1'

    page_number = int(page_number)
    return render(request, 'core/home.html', {'posts': posts,  'number': page_number, 'lastpost': lastpost, 'categories': categories, 'common_tags': common_tags})


def category_posts(request, slug_category):
    category = Category.objects.get(slug=slug_category)
    posts = Post.objects.filter(category=category)
    lastpost = posts.order_by('-id')[:3]
    common_tags = Post.tags.most_common()[:10]
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    print(type(page_number))
    if page_number == None:
        page_number = '1'

    page_number = int(page_number)
    print(category)
    print(posts)
    return render(request, 'core/category_posts.html', {'posts': posts, 'number': page_number, 'lastpost': lastpost, 'category': category, 'common_tags': common_tags})


def show_post_detail(request, slug_category, slug_post):
    category = Category.objects.get(slug=slug_category)
    post = Post.objects.get(slug=slug_post)
    comments = Comment.objects.filter(post__slug=slug_post).order_by('-id')
    # tag = None
    # if slug_tag :
    # tag = get_object_or_404(Tag, slug=post.tags.slug)
    # print('the tag is ', tag)
    #     common_posts= Post.objects.filter(tags__in=[tag])
    print(post.tags.all())
    post_tags_ids = Post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('same_tags', '-create_at')[:3]
    return render(request, 'core/postdetail.html', {'category': category, 'post': post, 'comments': comments, 'similar_posts': similar_posts})


# def tagged(request, slug):

#     tag = get_object_or_404(Tag, slug=slug)
#     comm_posts = Post.objects.filter(tags=tag)
#     return HttpResponse('')


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        currentuser = request.user
        if form.is_valid():
            obj = form.save(commit=False)
            obj.create_by = request.user
            obj.slug = slugify(obj.title)
            obj.save()
            form.save_m2m()
            return redirect('home')

    else:
        form = PostForm()
    return render(request, 'core/postform.html', {'form': form})


# def add_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         currentuser = request.user
#         if form.is_valid():

#             # form.save()
#             title = form.cleaned_data.get('title')
#             message = form.cleaned_data.get('message')
#             image = form.cleaned_data.get('image')
#             print('image idddddddddddd', image)
#             category = form.cleaned_data.get('category')
#             tags = form.cleaned_data.get('tags')
#             slug = slugify(title)
#             print('the tags are ', tags)
#             # print(type(tags))
#             # # print('the tags are ', tags.value)
#             post = Post.objects.create(
#                 title=title, category=category, message=message, image=image, create_by=currentuser, slug=slug, tags=tags).save()
#             # post.save_m2m()
#             # post.tags.add('o', 'p')
#             # post.save()
#             print('the title is : ', title)
#             print('the message is :', message)
#             # print('post request is done', form)

#     else:
#         form = PostForm()
#     return render(request, 'core/postform.html', {'form': form})


def tagged(request, slug):
    categories = Category.objects.filter(status="True")
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    posts = Post.objects.filter(tags=tag)
    lastpost = Post.objects.all().order_by('-id')[:3]
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    print(type(page_number))
    if page_number == None:
        page_number = '1'

    page_number = int(page_number)
    return render(request, 'core/home.html', {'posts': posts, 'number': page_number, 'lastpost': lastpost, 'categories': categories, 'common_tags': common_tags})


def add_comment(request, num_post):

    if request.user.is_authenticated:
        currentuser = request.user
        print('the request is', request.POST)
        post = Post.objects.get(id=num_post)

        print('comment', request.POST.get('comment'))
        if request.method == 'POST':

            comment_text = request.POST.get('comment')
            commenter = currentuser = request.user
            pro = UserProfile.objects.get(user=commenter)
            print('the crrent user isfffffffffffffffffffffffffffffff ', request.user)
            print(' the profile of comment writer is :',
                  commenter.profiles.city)
            comment = Comment.objects.create(
                comment=comment_text, commenter=commenter, post=post).save()

            return redirect('post_detail', post.category.slug, post.slug)
        # category = Category.objects.get(=slug_category)

        print(post.categorypost)
        comments = Comment.objects.filter(post__id=num_post)
        return render(request, 'core/postdetail.html', {'post': post, 'comments': comments})
    else:
        return redirect('login')


def delete_comment(request, num_post, num_comment):
    url = request.META.get('HTTP_REFERER')
    print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
    comment = Comment.objects.get(id=num_comment, post__id=num_post).delete()

    return HttpResponseRedirect(url)


@ login_required(login_url='/login')  # Check login
def addlike(request, num_post, num_comment):
    url = request.META.get('HTTP_REFERER')
    user = request.user

    comment_obj = Comment.objects.get(id=num_comment)

    if user in comment_obj.like.all():
        comment_obj.like.remove(user)

    else:
        comment_obj.like.add(request.user)

    like, created = Like.objects.get_or_create(
        user=user, comment_id=num_comment)
    if not created:
        if like.value == 'like':
            like.value = 'unlike'
        else:
            like.value = 'like'

        like.save()

    return HttpResponseRedirect(url)


@ login_required(login_url='/login')  # Check login
def favorite(request):
    comments_Favorite = Comment.objects.filter(like=request.user)

    return render(request, 'core/Favorite.html', {'comments': comments_Favorite})
