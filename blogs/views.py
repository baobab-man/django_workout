from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from blogs.models import Post, Comment

import json


def posts_list(request):
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogs/posts_list.html', context={'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post.id)

    return render(request, 'blogs/post_detail.html', context={'post': post, 'comments': comments})


@login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(user=request.user, title=title, content=content, image=image)

            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))
    
    return render(request, 'blogs/post_write.html', {'user': request.user, 'errors': errors})


@login_required
def comment_write(request):
    errors = []
    if request.method == 'POST':
        post_id = request.POST.get('post_id', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Comment.objects.create(user=request.user, post_id=post_id, content=content)

            return redirect(reverse('post_detail', kwargs={'post_id': comment.post.id}))
    
    return render(request, 'blogs/post_detail.html', {'user': request.user, 'errors': errors})
