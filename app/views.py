from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context import RequestContext

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


from user_app.forms import SignUpForm, PictureForm
from user_app.models import PictureModel, FollowModel

from post.models import PostModel

def main(request):
    #return render_to_response("main.html", {})
    return render_to_response('main.html', {}, context_instance=RequestContext(request))

def test_home(request):
    return render_to_response("home.html", {})
      
def test_help(request):
    return render_to_response("help.html", {})

def test_about(request):
    return render_to_response("about.html", {})

@login_required()
def home(request):
    entries = 0
    try:
        picture = PictureModel.objects.get(name=request.user.username)
    except ObjectDoesNotExist:
        picture = None
    try:
        entries = PostModel.objects.all().filter(user=request.user).count()
        if entries > 0:
            last = PostModel.objects.all().filter(user=request.user).order_by('id').reverse()[0]
            posts = PostModel.objects.all().filter(user=request.user).order_by('id').reverse()[1:6]
        else:
            last = None
            posts = None
    except ObjectDoesNotExist:
        posts = None

    try:
        following = FollowModel.objects.all().filter(user=request.user).order_by('id').reverse()
    except ObjectDoesNotExist:
        following = None
    try:
        followers = FollowModel.objects.all().filter(following=request.user).count()
    except ObjectDoesNotExist:
        followers = None
    fPic = []
    for f in following:
        try:
            fPic.append(PictureModel.objects.get(name=f.following.username))
        except ObjectDoesNotExist:
            fPic.append(None)
    fPost = []
    for f in following:
        try:
            if PostModel.objects.filter(user=f.following).count() != 0:
                fPost.append(PostModel.objects.filter(user=f.following).order_by('id').reverse()[0])
        except ObjectDoesNotExist:
            fPost.append(None)
    post = {
        'last':last,
        'posts':posts,
        'entries':entries,
    }
    if following.count() == None:
        countFollowing = 0
    else:
        countFollowing = following.count()
    if followers == None:
        followers = 0
    count = {
        'following':countFollowing,
        'followers':followers,
    }
    return render_to_response('home.html',
                            {'user': request.user, 'picture': picture, 'posts':post, 'count':count, 'data':zip(following,fPic,fPost)},
                            context_instance=RequestContext(request))

@login_required()
def post(request):
    entries = 0
    try:
        picture = PictureModel.objects.get(name=request.user.username)
    except ObjectDoesNotExist:
        picture = None
    try:
        entries = PostModel.objects.all().filter(user=request.user).count()
        if entries > 0:
            last = PostModel.objects.all().filter(user=request.user).order_by('id').reverse()[0]
            posts = PostModel.objects.all().filter(user=request.user).order_by('id').reverse()[1:6]
        else:
            last = None
            posts = None
    except ObjectDoesNotExist:
        posts = None

    try:
        following = FollowModel.objects.all().filter(user=request.user).count()
    except ObjectDoesNotExist:
        following = None
    try:
        followers = FollowModel.objects.all().filter(following=request.user).count()
    except ObjectDoesNotExist:
        followers = None

    if following == None:
        following = 0
    if followers == None:
        followers = 0
    count = {
        'following':following,
        'followers':followers,
    }
    post = {
        'last':last,
        'posts':posts,
        'entries':entries,
    }
    return render_to_response('post.html', {'user': request.user, 'picture': picture, 'posts':post, 'count':count },context_instance=RequestContext(request))

@login_required()
def following(request):
    try:
        picture = PictureModel.objects.get(name=request.user.username)
    except ObjectDoesNotExist:
        picture = None

    try:
        following = FollowModel.objects.all().filter(user=request.user).order_by('date').reverse()
    except ObjectDoesNotExist:
        following = None
    fPic = []
    for f in following:
        try:
            fPic.append(PictureModel.objects.get(name=f.following.username))
        except ObjectDoesNotExist:
            fPic.append(None)

    return render_to_response('following.html', {'user': request.user, 'picture': picture, 'data':zip(following,fPic) },context_instance=RequestContext(request))

@login_required()
def followers(request):
    try:
        picture = PictureModel.objects.get(name=request.user.username)
    except ObjectDoesNotExist:
        picture = None

    try:
        followers = FollowModel.objects.all().filter(following=request.user).order_by('date').reverse()
    except ObjectDoesNotExist:
        followers = None
    fPic = []
    for f in followers:
        try:
            fPic.append(PictureModel.objects.get(name=f.user.username))
        except ObjectDoesNotExist:
            fPic.append(None)

    return render_to_response('followers.html', {'user': request.user, 'picture': picture, 'data':zip(followers,fPic) },context_instance=RequestContext(request))

##### PAGINAS ESTATICAS
def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))

def aboutIntern(request):
    return render_to_response('about2.html', {}, context_instance=RequestContext(request))

def help(request):
    return render_to_response('help.html', {}, context_instance=RequestContext(request))

def helpIntern(request):
    return render_to_response('help2.html', {}, context_instance=RequestContext(request))