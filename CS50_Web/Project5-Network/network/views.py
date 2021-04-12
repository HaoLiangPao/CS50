from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Tweet, Comment


def index(request):
    # Fetch all posts from database
    posts = list(Tweet.objects.all())
    # Order by timestamp (increasing)
    def get_timestamp(post):
        post.timestamp = post.timestamp.strftime("%b %d %Y, %I:%M %p")
        return post.timestamp
    posts.sort(key=get_timestamp)
    return render(request, "network/index.html", {
        "posts": posts
    })


def profile(request, username):
    # Check if current user is the user whose profile been accessed
    profile_user = User.objects.get(username=username)
    if profile_user != request.user:
        sameUser = False
        # Check if the logged in user already follow the profile user
        following = request.user.following.all()
        if profile_user in following:
            allow_follow = True
        else:
            allow_follow = False
    else:
        sameUser = True
        allow_follow = False
    # Number of followers and user followings
    followers = len(request.user.following.all())
    following = len(request.user.follower.all())
    # All posts created by this user
    posts = Tweet.objects.filter(user=request.user)
    
    return render(request, "network/profile.html", {
        "username": request.user.username,
        "following": following,
        "followers": followers,
        "posts": posts,
        "allowFollow": allow_follow,
        "sameUser": sameUser
    })


def follow(request, username):
    if request.method == "PUT":
        # Get user to be followed
        targetUser = User.objects.get(username=username)
        # Follow user
        request.user.following.add(targetUser)
        return HttpResponseRedirect(reverse("profile", args=(username)))
    return HttpResponseRedirect(reverse("index"))


def unfollow(request, username):
    if request.method == "POST":
        # Get user to be followed
        targetUser = User.objects.get(username=username)
        # Follow user
        request.user.following.remove(targetUser)
        return HttpResponseRedirect(reverse(profile, args=(username)))
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def new_post(request):
    if request.method == "POST":
        # Get user input
        content = request.POST["content"]
        # Save the post (with default timestamp and 0 likes)
        print(request.user)
        tweet = Tweet(user=request.user, body=content, likes=0)
        tweet.save()
        # Success message
        message = "Tweet successfully posted!"
        return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
