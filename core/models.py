from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length=50)

    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True, allow_unicode=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def get_category():
    return Category.objects.get(id=1)


class Post(models.Model):

    title = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        Category, default=get_category, related_name="categoryPost", on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(
        upload_to='images/', default='images/404.png', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True,
                            unique=True, allow_unicode=True)
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return str((self.title))
        # return Truncator(self.message).chars(15)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.category.slug, self.slug])

    @property
    def ago(self):
        # ag = timezone.now() - self.create_at
        ag = timezone.now()
        return ag 
        # return timezone.localtime(ag).strftime("%Y-%m-%d %H:%M:%S")


class Comment(models.Model):
    comment = models.TextField(null=True)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='favourite', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.commenter} commented on {self.post}"


LIKE_CHOICES = (('like', 'like'), ('unlike', 'unlike'))


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name='likecomment', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='unlike', max_length=10)

    def __str__(self):
        return str(self.comment)
