# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(u"Заголовок", max_length=200)
    text = models.TextField(u"Содержание")
    pub_date = models.DateTimeField(u"Дата публикации")

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User, verbose_name=u"Пользователь")
    pub_date = models.DateTimeField(u"Дата публикации")
    text = models.TextField(u"Содержание")

    def __unicode__(self):
        trailer = ""
        if len(self.text) > 50:
            trailer = "..."
        return self.text[:50] + trailer
