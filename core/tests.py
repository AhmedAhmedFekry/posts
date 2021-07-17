from django.test import Client, SimpleTestCase, TestCase, override_settings
from .models import Category ,Post ,Comment ,Like , get_category
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime
class CategoryTest(TestCase):
    def category_create(self):
        return Category.objects.create(title='front',status='True',slug='front')


    def test_model_str(self):
        category=self.category_create()
        self.assertEqual(category.__str__(),category.title)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PostTest(TestCase):
    # category1=Category.objects.create(title='front2h5',status='True',slug='frontsh5')

    # create_by=User.objects.create(username='ahmmed5hs0',password='2c5d5d176dd')
    def post_create(self):
        category1=Category.objects.create(title='front2h50',status='True',slug='frontsh502')
        self.ad = timezone.now()
        create_by=User.objects.create(username='ahmmed5hs120',password='2c5d5d555176dd')

        return Post.objects.create(title='frontsdhss',message="lllll",slug='lfrdont',create_by=create_by,tags='django',category= category1)


    def test_model_str(self):
        post=self.post_create()
        self.assertEqual(post.__str__(),post.title)
# 'category/<slug:slug_category>/<slug:slug_post>/'
    def test_get_absolute_url(self):
        # post= Post.objects.get(id=1)
        # self.assertEqual(post.get_absolute_url,f"{post.category.title}/{post.category.slug}/{}" )

        post=self.post_create()
        first_category_url = f"/category/{post.category.slug}/{ post.slug}/"
        self.assertEqual(first_category_url, post.get_absolute_url()) 
    def test_ago(self):
        post=self.post_create()
        commenter= User.objects.create(username='ahmedmmmm',password='2f2f8vgr85')
        self.assertEqual(post.ago.strftime("%Y-%m-%d %H:%M:%S"),self.ad.strftime("%Y-%m-%d %H:%M:%S"))
        # response = self.client.post(reverse('post_detail', args=[post.category.slug, post.slug,])) #set unit_view to the url name in the urls.py
class CommentTest(TestCase):
    def comment_create(self):
        category1=Category.objects.create(title='front2dh50',status='True',slug='frontxsh502')
        commenter=User.objects.create(username='ahmmed5fhsd120',password='2c5d5d55dff5176dd')
        post=Post.objects.create(title='frontsdhss',message="lllll",slug='lfrdont',create_by=commenter,tags='django',category= category1)
        
        return Comment.objects.create(comment='fffffffff',post=post,commenter=commenter, active=True)
    def test_model_str(self):
        comment=self.comment_create()
        self.assertEqual(comment.__str__(),f"{comment.commenter} commented on {comment.post}")

class LikeTest(TestCase):
    def like_create(self):
        category1=Category.objects.create(title='front2dhf50',status='True',slug='fronftxsh502')
        commenter=User.objects.create(username='ahmmed5fhfsd120',password='2c5d5d55dfff5176dd')
        post=Post.objects.create(title='frontsdhfss',message="lllll",slug='lfrfdont',create_by=commenter,tags='django',category= category1)
        comment=Comment.objects.create(comment='fffffffff',post=post,commenter=commenter, active=True)
        return Like.objects.create(user=commenter,comment=comment,value='unlike')

    def test_model_str(self):
        like=self.like_create()
        self.assertEqual(like.__str__(),like.comment.__str__())

class ViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        category1=Category.objects.create(title='front8',status='True',slug='front8')
        create_by=User.objects.create(username='ahmmed5hs1240',password='2c5d5d5555176dd')
        post=Post.objects.create(title='frontsdhss',message="lllll",slug='lfrdont',create_by=create_by,tags='django',category= category1)
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_home_page(self):
        response= self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_category_posts(self):
        """
        Test category posts response status
        """
        response = self.c.get(
            reverse('category_post', args=['front8']))
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_show_post_detail(self):
        """
        Test category posts response status
        """
        response = self.c.get(
            reverse('post_detail', args=['front8','lfrdont']))
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_add_post(self):
        data={'title':'Git Tutorial1','category':"Preparation",'message':'vvv','tags':'git python'}
        response= self.client.get(reverse('add_post'))
        response= self.client.post(reverse('add_post'),data)
        self.assertEqual(response.status_code, 200)


    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_tagged(self):
        # response= self.client.get(reverse('tagged',args=('django',)))
        # response= self.client.get(reverse('tagged',kwargs={'slug':'django'}))
        response= self.client.get('http://127.0.0.1:8000/tag/github/')
        
        self.assertEqual(response.status_code, 404)
      
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_add_comment(self):
        # self.client.login(username='admin', password='admin')
        category1=Category.objects.create(title='fronct8',status='True',slug='froccnt8')
        create_by=User.objects.create(username='ahmmced5hs1240',password='2c5d5d55c55176dd')
        post=Post.objects.create(title='frontcsdhss',message="llclll",slug='lfrdcont',create_by=create_by,tags='django',category= category1)
        data={'comment':'Git Tutorial1','post':post,'commenter':create_by}
        response= self.client.post(reverse('add_comment',args=[1]),data)
        # response= self.client.post(reverse('add_post'),data)
        self.assertEqual(response.status_code, 200)
