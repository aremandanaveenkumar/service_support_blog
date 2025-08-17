from django.contrib import admin
from .models import AddressField, Post, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'problem_reported', 'rectification', 'customer']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('problem_reported', 'rectification',)


# Register your models here.
admin.site.register(AddressField)
admin.site.register(Comment)


