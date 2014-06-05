from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from user_app.forms import SignUpForm, PictureForm
from user_app.models import PictureModel, FollowModel
from post.models import PostModel

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            userAuth = authenticate(username=username, password=password)
            if userAuth is not None:
                if userAuth.is_active:
                    login(request, userAuth)
            entries = 0
            post = {
                'entries':entries,
            }
            return render_to_response('home.html', {'user': user, 'posts': post}, context_instance=RequestContext(request))
    else:
        form = SignUpForm()
 
    data = {
        'form': form,
    }
    return render_to_response('main.html', data, context_instance=RequestContext(request))


@login_required()
def profile(request):
    try:
        picture = PictureModel.objects.get(name=request.user.username)
    except ObjectDoesNotExist:
        picture = None
    form = SignUpForm()
    return render_to_response('profile.html', {'user': request.user, 'picture': picture, 'form': form},context_instance=RequestContext(request))

@login_required
def savePicture(request):
	if request.method == 'POST':
		form = PictureForm(request.POST, request.FILES)
		if(form.is_valid):
			try:
				picture = PictureModel.objects.get(name=request.user.username)
			except ObjectDoesNotExist:
				picture = PictureModel(name=request.user.username)
			picture.picture = request.FILES['upload']
			picture.save()
			return HttpResponseRedirect(reverse('profile'))

@login_required()
def updateProfile(request):
    if request.method == 'POST':
        user = request.user
        if request.POST.get('username'):
            try:
                oldUser = User.objects.get(username=request.POST.get('username'))
            except ObjectDoesNotExist:
                oldUser = None
            if oldUser == None:
                try:
                    picture = PictureModel.objects.get(name=user.username)
                    picture.name = request.POST.get('username')
                    picture.save()
                except:
                    picture = None
                user.username = request.POST.get('username')
            else:
                try:
                    picture = PictureModel.objects.get(name=user.username)
                except ObjectDoesNotExist:
                    picture = None
                data = {
                    'error': True,
                    'username': request.POST.get('username'),
                }
                return render_to_response('profile.html', {'data': data, 'picture': picture},context_instance=RequestContext(request))
        if request.POST.get('email'):
            user.email = request.POST.get('email')
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
        if request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
        user.save()
        try:
            picture = PictureModel.objects.get(name=user.username)
        except ObjectDoesNotExist:
            picture = None
        data = {
            'error': False,
            'username': request.POST.get('username'),
        }
        return render_to_response('profile.html', {'data': data, 'picture': picture},context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('profile'))


@login_required()
def updatePassword(request):
    if request.method == 'POST':
        user = request.user
        response_data = {}
        if request.POST.get('new_password') == request.POST.get('confirm_password'):
            user.set_password(request.POST.get('new_password'))
            user.save()
            error = False
        else:
            error = True
        return render_to_response('profile.html', {'error': error},context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('profile'))    

@login_required()
def deleteProfile(request):
    if request.method == 'POST':
        user = request.user
        try:
            picture = PictureModel.objects.get(name=user.username)
            picture.delete()
            posts = PostModel.objects.all().filter(user=user)
            posts.delete()
        except:
            picture = None
        try:
            posts = PostModel.objects.all().filter(user=user)
            posts.delete()
        except:
            posts = None
        user.delete()
        return HttpResponseRedirect(reverse('main'))


def follow(request):
    if request.method == 'POST':
        if request.user.username != request.POST.get('followname'):
            follow = User.objects.get(username=request.POST.get('followname'))
            try:
                check = FollowModel.objects.get(user=request.user,following=follow)
            except ObjectDoesNotExist:
                link = FollowModel(user=request.user,following=follow)
                link.save()
    return HttpResponseRedirect(reverse('home'))


def unfollow(request):
    if request.method == 'POST':
        follow = User.objects.get(pk=request.POST.get('delname'))
        try:
            link = FollowModel.objects.get(user=request.user,following=follow)
            link.delete()
        except ObjectDoesNotExist:
            link = None
    return HttpResponseRedirect(reverse('home'))

def searchUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return search(request,username)

def search(request, username):
    data = None
    post = None
    try:
        user = User.objects.get(username=username);
    except ObjectDoesNotExist:
        user = None
        return HttpResponseRedirect(reverse('home'))
    if user != None:
        try:
            picture = PictureModel.objects.get(name=user.username)
        except:
            picture = None
        try:
            entries = PostModel.objects.all().filter(user=user).count()
            if entries > 0:
                last = PostModel.objects.all().filter(user=user).order_by('id').reverse()[0]
                posts = PostModel.objects.all().filter(user=user).order_by('id').reverse()[1:6]
            else:
                last = None
                posts = None
        except ObjectDoesNotExist:
            posts = None
        if request.user.username != username:
            try:
                link = FollowModel.objects.get(user=request.user,following=user)
            except ObjectDoesNotExist:
                link = None
        else:
            link = False
        post = {
            'last':last,
            'posts':posts,
            'entries':entries,
        }
        data = {
            'user':user,
            'picture':picture,
        }
    return render_to_response('search.html', {'data': data, 'post': post, 'link': link},context_instance=RequestContext(request))