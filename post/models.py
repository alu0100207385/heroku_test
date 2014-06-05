from django.db import models
from datetime import date                                                                                                             
from django.contrib.auth.models import User

class PostModel(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField(default=date.today)
	post = models.CharField(max_length=240)
	class Meta:
	  app_label = 'post'

