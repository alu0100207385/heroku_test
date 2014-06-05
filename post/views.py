from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from post.models import PostModel

import re

def createPost(request):
	if request.method == 'POST':
		post = PostModel(user=request.user,post=request.POST.get('post'))
		post.save()
		if re.search("/home",request.META.get('HTTP_REFERER')):
			return HttpResponseRedirect(reverse('home'))
		elif re.search("/post/",request.META.get('HTTP_REFERER')):
			return HttpResponseRedirect(reverse('post'))
	return HttpResponseRedirect(reverse('home'))


def updatePost(request):
	if request.method == 'POST':
		post = PostModel.objects.get(pk=request.POST.get('id'))
		post.post = request.POST.get('post')
		post.save()
		if re.search("/home",request.META.get('HTTP_REFERER')):
			return HttpResponseRedirect(reverse('home'))
		elif re.search("/post/",request.META.get('HTTP_REFERER')):
			return HttpResponseRedirect(reverse('post'))
	return HttpResponseRedirect(reverse('home'))

def deletePost(request):
	if request.method == 'POST':
		post = PostModel.objects.get(pk=request.POST.get('id'))
		post.delete()
		if re.search("/home",request.META.get('HTTP_REFERER')):
			return HttpResponseRedirect(reverse('home'))
		elif re.search("/post/",request.META.get('HTTP_REFERER')):
			return HttpResponseRedirect(reverse('post'))
	return HttpResponseRedirect(reverse('home'))
