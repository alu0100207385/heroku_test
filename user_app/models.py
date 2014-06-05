from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import register


class PictureModel(models.Model):
	date = models.DateField(default=date.today)
	name = models.CharField(max_length=255)
	picture = models.ImageField(upload_to='profile/')
	class Meta:
	  app_label = 'user_app'

class FollowModel(models.Model):
	user = models.ForeignKey(User,related_name='user')
	following = models.ForeignKey(User,related_name='following')
	date = models.DateField(default=date.today)
	class Meta:
		app_label = 'user_app'