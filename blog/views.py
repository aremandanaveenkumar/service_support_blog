from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import Post, Comment, AddressField
from .forms import CommentForm, PostForm, AddressForm


class PostDrafts(generic.ListView):
    queryset = Post.objects.all().filter(status=0)
    template_name = "blog/index.html"
    paginate_by = 6

    def get_queryset(self):
        author = self.kwargs.get('author')
        if author:
            user = get_object_or_404(User, username=author)
            return Post.objects.filter(author=user, status=0)
        return Post.objects.all().filter(status=0)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.kwargs.get('author')
        if author:
            context['author'] = author
        return context


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.all().exclude(status=0).exclude(status=99)
    template_name = "blog/index.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        author_id = self.request.GET.get("user")

        if query:
            queryset = queryset.filter(title__icontains=query)
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["selected_user"] = self.request.GET.get("user", "")
        context["users"] = User.objects.all()
        return context


def post_detail(request, slug):
    """
    Display an individual :model:'blog.Post'.

    **Context**

    ''post''
        An instance of :model:'blog.Post'.

    **Template:**

    :template:'blog/post_detail.html'
    """
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)
    comments_all = post.comments.all().order_by("-created_on")
    comments = comments_all.filter(approved=True)
    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
                )
    comment_form = CommentForm()
    return render(request, "blog/post_detail.html", 
                  {
                    "post": post,
                    "comments": comments,
                    "comment_count": comment_count,
                    "comment_form": comment_form,
                    },
                  )


def add_address(request):
    """
    add new customer address
    """
    if request.method == "POST":
        address_form = AddressForm(data=request.POST)
        if address_form.is_valid() and any(address_form.cleaned_data.values()):
            existing_address = AddressField.objects.filter(
                street=address_form.cleaned_data.get("street"), 
                city=address_form.cleaned_data.get("city"), 
                state=address_form.cleaned_data.get("state"), 
                postal_code=address_form.cleaned_data.get("postal_code"), 
                country=address_form.cleaned_data.get("country")
                ).first()

            if not existing_address:
                address_form.save()
                return HttpResponseRedirect(reverse('post_create'))  
    else:
        address_form = AddressForm()

    return render(
        request,
        "blog/add_address.html",
        {
            "address_form": address_form,
        },
    )


def post_create(request):
    """
    create new post
    """
    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            slug = slugify(post.title)
            post.slug = slug
            post.author = request.user
            post.save()
            messages.add_message(request, 
                                 messages.SUCCESS, "Post Created.")
            return HttpResponseRedirect(reverse('post_detail', 
                                                args=[slug]))    

    else:
        post_form = PostForm()

    return render(
        request,
        "blog/post_create.html",
        {
            "post_form": post_form,
            "is_create": True
        },
    )


def post_edit(request, slug):
    """
    edit post
    """
    queryset = Post.objects.all()
    editpost = get_object_or_404(queryset, slug=slug)
    
    if request.method == "POST":
        editpost.delete()
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            slug = slugify(post.title)
            post.slug = slug
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    else:
        post_form = PostForm(instance=editpost)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            slug = slugify(post.title)
            post.slug = slug
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        
    return render(
        request,
        "blog/post_create.html",
        {
            "post_form": post_form,
            "is_create": False
        },
    )


def post_delete(request, slug):
    """
    delete Post
    """
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)

    if post.author == request.user:
        post.status = 99
        post.save()
        messages.add_message(request, messages.SUCCESS, 
                             'Admin Informed for deletion, if the reason is valid, it shall be processed!')
    else:
        messages.add_message(request, messages.ERROR, 
                             'You can only request to delete your own Posts!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 
                             'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

