# -*- coding: utf-8 -*-

import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.utils import timezone, formats

from blog.models import Post, Comment

def index(request):
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 4)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}
    return render(request, 'blog/base_posts.html', context)

def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/base_post.html', {'post': post})

def get_comments(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return_json = []
    for comment in post.comment_set.all():
        comment_json = {}
        comment_json['text'] = comment.text
        comment_json['user'] = comment.user.username
        comment_json['date'] = "%s %s" % (formats.date_format(comment.pub_date), 
                formats.time_format(comment.pub_date))
        return_json.append(comment_json)
    return HttpResponse(json.dumps(return_json), content_type='application/json')

def post_comment(request):
    return_json = {}
    formatted_date = ""
    if request.user.is_authenticated:
        post_id = request.POST['post']
        text = request.POST['text']
        try:
            post = get_object_or_404(Post, pk=int(post_id))
        except ValueError:
            return_json = {'status': 0, 'error': u'Не существует такой записи'}
            return HttpResponse(json.dumps(return_json), mimetype='application/json')
        if text and len(text.strip()) > 0:
            comment = Comment(user=request.user, 
                    pub_date=datetime.datetime.now(), 
                    text=text, 
                    post=post)
            comment.save()
            return_json = {'status': 1, 'date': "%s %s" % (formats.date_format(comment.pub_date), 
                    formats.time_format(comment.pub_date))}
        else:
            return_json = {'status': 0, 'error': u'Текст комментария не может быть пустым'}
    else:
        return_json = {'status': 0, 'error': u'Вы должны быть зарегистрированы, чтобы оставить комментарий'}
    return HttpResponse(json.dumps(return_json), content_type='application/json')

def profile(request):
    return render(request, 'blog/base_profile.html')
