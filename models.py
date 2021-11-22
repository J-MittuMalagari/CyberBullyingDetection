from django.db import models

from django.db.models import Model

class RegistrationModel(Model):

    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    pic=models.FileField(upload_to="images")

class PostModel(models.Model):

    username = models.CharField(max_length=60)
    title = models.CharField(max_length=30)
    image = models.FileField(upload_to="images")
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)

class CommentModel(models.Model):

    post = models.CharField(max_length=60)
    comment = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    username = models.CharField(max_length=60)

class LikeOrDisLikeModel(models.Model):

    post = models.CharField(max_length=60)
    status = models.CharField(max_length=100)
    username = models.CharField(max_length=60)

class ShareModel(models.Model):

    username = models.CharField(max_length=60)
    post = models.CharField(max_length=60)

class FriendRequestModel(models.Model):

    username = models.CharField(max_length=60)
    friendname = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    status = models.CharField(max_length=60)