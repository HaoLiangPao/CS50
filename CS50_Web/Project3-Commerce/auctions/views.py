from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Comment, Bid


def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def watchList(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def create(request):
    # When form is submitted
    if request.method == "POST":
        # Get form input
        title = request.POST[title]
        start_bid = request.POST[bid]
        image_url = request.POST[image] if request.POST[image] else ""
        description = request.POST[description]
        # Get created time
        # Create a date string with a certain standard
        now = datetime.now()
        year, minute, day = now.year, now.minute, now.day
        month = monthConverter(int(now.month))
        hour = int(now.hour)
        if hour > 12:
            hour -= 12
            end = "p.m."
        else:
            end = "a.m."
        time = f"{month} {day}, {year}, {hour}:{minute} {end}"
        # Check for missing value
        if title and start_bid and description and image_url and time:
            # Create auction listing
            auction = Auction(title=title, description=description, start_bid=start_bid, image=image_url, created=time)
            autction.save()

        # If missing value
        else:
            return render(request, "auctions/create.html", {
                "message" : "Please fill in all the blanks except image URL."
            })
    # Normal case
    return render(request, "auctions/create.html")


# -- Helper functions --
def monthConverter(month):
    months = {
        1: "Jan.",
        2: "Feb.",
        3: "Mar.",
        4: "Apr.",
        5: "May",
        6: "June",
        7: "July",
        8: "Aug.",
        9: "Sept.",
        10: "Oct.",
        11: 'Nov.',
        12: "Dec."
    }
    return months[month]



