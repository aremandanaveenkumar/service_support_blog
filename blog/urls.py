from . import views
from django.urls import path
from django.contrib.auth.models import User

urlpatterns = [
    path("", views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/drafts/<str:author>', views.PostDrafts.as_view(), name='drafts'),    
    path('post/edit/<slug:slug>', views.post_edit, name='post_edit'),
    path('post/delete/<slug:slug>', views.post_delete, name='post_delete'),
    path('add_address', views.add_address, name='add_address'),
    path('<slug:slug>/edit_comment/<int:comment_id>', 
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
]