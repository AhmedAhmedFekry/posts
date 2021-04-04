from django import forms
from core.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'image', 'message', 'tags')
