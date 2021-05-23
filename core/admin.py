from django.contrib import admin
from .models import Post, Comment, Like, Category
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class CommentAdmin(ImportExportModelAdmin):
    list_display = ['comment', 'post', "commenter", ]


class LikeAdmin(ImportExportModelAdmin):
    list_display = ['comment', 'user']


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['title', 'status']
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(ImportExportModelAdmin):
    list_display = ['title', 'category', 'create_at']
    date_hierarchy = 'create_at'
    # raw_id_fields = ('category',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
