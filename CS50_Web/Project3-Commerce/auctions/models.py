from django.contrib.auth.models import AbstractUser
from django.db import models

# A default generator for arrays
def my_default():
    return [-1]

class User(AbstractUser):
    # Array of auction objects' id
    auctions = models.JSONField(default=my_default)
    # Array of bid objects' id
    watchList = models.JSONField(default=my_default)

    def __str__(self):
            return f"{self.username}({self.id})"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.FloatField()
    image = models.URLField()
    createdAt = models.CharField(max_length=26)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owns")

    def __str__(self):
        return f"{self.title} ({self.start_bid})"

class Category(models.Model):
    # a user place a new bid on a listing
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"category{self.id}: \n category({self.category}"

class Auction_Category(models.Model):
    listing_id = models.IntegerField()
    category_id = models.IntegerField()

    def __str__(self):
        return f"listing_id({self.listing_id}) -> category({self.category_id})"

class Comment(models.Model):
    # A user makes a comment on a listing
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    content = models.TextField()
    def __str__(self):
        return f"user({self.user}) puts a new comment on listing({self.listing})"


class Bid(models.Model):
    # a user place a new bid on a listing
    user = models.IntegerField()
    listing = models.IntegerField()
    new_bid = models.FloatField()

    def __str__(self):
        return f"user({self.user}) puts a new_bid({self.new_bid} on listing({self.listing})"
