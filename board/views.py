from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm


def index(request):
    return render(request, "index.html")


def post_list(request):
    query = request.GET.get("q", "")
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "board/list.html", {"posts": posts, "query": query})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, "board/detail.html", {"post": post, "comment_form": comment_form})


def post_write(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("board:list")
    else:
        form = PostForm()
    return render(request, "board/write.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("board:detail", pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, "board/write.html", {"form": form, "edit": True})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("board:list")
    return render(request, "board/delete_confirm.html", {"post": post})


def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
    return redirect('board:detail', pk=post_pk)


def comment_write(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect("board:detail", pk=pk)
