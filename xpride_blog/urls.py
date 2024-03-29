from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from blog import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xpride_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)
