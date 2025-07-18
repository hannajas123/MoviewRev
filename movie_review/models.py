
from django.utils import timezone
from datetime import timedelta
from django.db import models


def default_time_plus_10():
    return timezone.now() + timedelta(minutes=10)

class Login(models.Model):
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    salt=models.CharField(max_length=255)

class Movies(models.Model):
    name=models.CharField(max_length=255)
    photo=models.FileField(upload_to='media/img',null=True)
    language=models.CharField(max_length=255,default="")
    release_date=models.DateField(default="2025-5-14")
    actors=models.CharField(max_length=255,default="")
    director=models.CharField(max_length=255,default="")
    writer=models.CharField(max_length=255,default="")
    discription=models.CharField(max_length=550,default="")
    categories_tags = models.CharField(max_length=500,default="")

class Users(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    photo=models.FileField(upload_to='media/img',null=True)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)

class Reviews(models.Model):
    review=models.CharField(max_length=555)
    time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='review_user_id')
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='review_movie_id')

class Saved(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='saved_user_id')
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='saved_movie_id')
 
class Rating(models.Model):
    rate=models.FloatField()
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='rated_user_id')
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='rated_movie_id')

class Likes(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='liked_user_id')
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='liked_movie_id')

class Dislikes(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='disliked_user_id')
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='disliked_movie_id')    

class Search(models.Model):
    search=models.CharField(max_length=255)
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='searched_user_id')

class ForgotPassword(models.Model):
    token=models.CharField(max_length=255)
    start_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField(default=default_time_plus_10)
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='forgot_password_user_id')
    is_used=models.BooleanField(default=False)
    secret=models.CharField(max_length=255,default="")
