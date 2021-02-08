from django.contrib.auth.models import AbstractUser
from django.db import models

# A default generator for arrays
def my_default():
    return [-1]

class User(AbstractUser):
    # Array of auction objects
    auctions = models.JSONField(default=my_default)
    # Array of bid objects
    bids = models.JSONField(default=my_default)
    # Array of comments objects (string)
    comments = models.JSONField(default=my_default)


class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.FloatField()
    image = models.URLField()
    created = models.CharField(max_length=26)

    def __str__(self):
        return f"listing{self.id}: \ntitle({self.title})\n start_bid({self.start_bid}"


class Comment(models.Model):
    # A user makes a comment on a listing
    user = models.IntegerField()
    listing = models.IntegerField()
    content = models.TextField()
    def __str__(self):
        return f"comment{self.id}: \nlisting({self.listing})\n content({self.content}"


class Bid(models.Model):
    # a user place a new bid on a listing
    user = models.IntegerField()
    listing = models.IntegerField()
    new_bid = models.FloatField()

    def __str__(self):
        return f"bid{self.id}: \nlisting({self.listing})\n new_bid({self.content}"
