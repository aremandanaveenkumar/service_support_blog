from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 
                  'customer', 'customer_address', 'problem_reported', 
                  'rectification', 'status', 'excerpt']
        exclude = ['slug', ]
        widgets = {'problem_reported': SummernoteWidget(),  
                   'rectification': SummernoteWidget()}
        
