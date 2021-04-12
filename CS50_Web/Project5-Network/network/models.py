from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following")
    followings = models.ManyToManyField('self', symmetrical=False, related_name="follower")
    def __str__(self):
        return f"{self.username}({self.id})"

class Tweet(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tweets_made")
    body = models.TextField(blank=True)
    likes = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Tweet: {self.id} (made by {self.user})"

class Comment(models.Model):
    user = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comments_given")
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="comments_received")
    body = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment #({self.id})"