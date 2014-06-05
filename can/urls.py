from django.conf.urls import patterns, include, url
#from app.views import test_home
from app.views import *
#from app.views import test_about, test_help,
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'app.views.main', name='main'),
    url(r'^signup$', 'user_app.views.signup', name='signup'),
    url(r'^login$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^logout$', logout, {'template_name': 'main.html', }, name="logout"),

    url(r'^home$', 'app.views.home', name='home'),
    url(r'^post/$', 'app.views.post', name='post'),
    url(r'^following/$', 'app.views.following'),
    url(r'^followers/$', 'app.views.followers'),

    # Paginas estaticas: help, about, developers...
    url(r'^about/$', 'app.views.about'),
    url(r'^about2/$', 'app.views.aboutIntern'),
    url(r'^help/$', 'app.views.help'),
    url(r'^help2/$', 'app.views.helpIntern'),

    # Paginas de la app: user_app
    url(r'^profile/$', 'user_app.views.profile', name="profile"),
    url(r'^uploadPic/$', 'user_app.views.savePicture'),
    url(r'^updateProfile/$', 'user_app.views.updateProfile'),
    url(r'^updatePassword/$', 'user_app.views.updatePassword'),
    url(r'^deleteProfile/$', 'user_app.views.deleteProfile', name='deleteProfile'),
    url(r'^search/$', 'user_app.views.searchUser', name='search'),
    
    # Paginas de follow:
    url(r'^follow/$', 'user_app.views.follow'),
    url(r'^unfollow/$', 'user_app.views.unfollow'),
    url(r'^users/(?P<username>[-\w]+)/$', 'user_app.views.search'),


    # Paginas de la app: post
    url(r'^createPost/$', 'post.views.createPost'),
    url(r'^updatePost/$', 'post.views.updatePost'),
    url(r'^deletePost/$', 'post.views.deletePost'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls))
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    
