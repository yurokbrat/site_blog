from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from users.models import Profile
from django.db.models import Count
from .forms import CommentForm


def home(request):
    posts = Post.objects.annotate(comment_count=Count("comment")).all()
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-data_posted"]
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        comments = Comment.objects.filter(post=post).order_by("-created")
        form = CommentForm()
        return render(
            request,
            "blog/post_detail.html",
            context={"post": post, "comments": comments, "form": form},
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("post_detail", pk=post.pk)
        else:
            comments = Comment.objects.filter(post=post)
            return render(
                request,
                "blog/post_detail.html",
                context={"form": form, "post": post, "comments": comments},
            )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteViews(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-data_posted")


class TopUsersView(ListView):
    model = Profile
    template_name = "blog/user_top.html"
    context_object_name = "top_users"
    ordering = ["-post_count"]

    def get_queryset(self):
        return Profile.objects.annotate(post_count=Count("user__post")).order_by(
            "-post_count"
        )[:10]


def about(request):
    return render(request, "blog/about.html", context={"title": "YuroKeep"})
