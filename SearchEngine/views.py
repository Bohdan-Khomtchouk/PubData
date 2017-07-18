from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from SearchEngine.lib.utils import find_search_result
from .models import SearchQuery, Recommendation, ServerName
from .forms import SearchForm, SelectServer
from ast import literal_eval
from django.views.decorators.csrf import csrf_exempt


def home(request):
    recommendations = Recommendation.objects.all()
    return render(request, 'SearchEngine/base.html', {'recoms': recommendations})


@csrf_exempt
def search_result(request):
    # query = get_object_or_404(Search, pk=pk)
    keyword = request.POST.get('keyword')
    selected = request.POST.get('selected')
    print(selected)
    search_model = SearchQuery()
    search_model.user = request.user
    search_model.add(word=keyword, servers=selected)

    result = find_search_result(keyword=keyword, servers=selected)
    # set recommendation table here!!

    return render(request, 'SearchEngine/search_result.html', {'all_paths': result})


@csrf_exempt
@login_required
def search(request):
    search_form = SearchForm()
    servers = ServerName.objects.all()
    return render(request, 'SearchEngine/search.html',
                  {'search_form': search_form, 'servers': servers})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'SearchEngine/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'SearchEngine/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'SearchEngine/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)