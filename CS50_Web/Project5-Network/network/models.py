from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name="following", symmetrical=False)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    def __str__(self):
        return f"{self.username}({self.id})"

class Tweet(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tweets_made")
    comments = models.ManyToManyField("Comment", related_name="comments_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "sender": self.sender.email,
    #         "recipients": [user.email for user in self.recipients.all()],
    #         "subject": self.subject,
    #         "body": self.body,
    #         "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
    #         "read": self.read,
    #         "archived": self.archived
    #     }
    
    def __str__(self):
        return f"Tweet: {self.id} (made by {self.user})"

class Comment(models.Model):
    user = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comments_given")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)