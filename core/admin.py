from django.contrib import admin
from .models import Post, Comment, Like, Category
# Register your models here.


class LikeAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'create_at']
    date_hierarchy = 'create_at'
    # raw_id_fields = ('category',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)
