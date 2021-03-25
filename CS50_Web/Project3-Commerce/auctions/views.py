from django.contrib.auth import authenticate, login, logout
# Private Routes middleware
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Auction, Comment, Bid

def index(request):
    # Get all active listing
    try:
        current_user = User.objects.get(id=request.user.id)
        try:
            auctions = Auction.objects.all()
        except Auction.DoesNotExist:
            print("No auctions.")
        myAuctions = []
        for auctionId in current_user.auctions:
            try:
                auction = Auction.objects.get(id=auctionId)
                myAuctions.append(auction)
            except Auction.DoesNotExist:
                print(f"No auction with id({auctionId}) exists")
        return render(request, "auctions/index.html", {
            "auctions": auctions,
           "myAuctions": myAuctions 
        })
    except User.DoesNotExist:
        print(f"No user logged in")
    

    return render(request, "auctions/index.html", {"message": "Please login to see active listings..."})

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

@login_required(redirect_field_name="my_redirect_field", login_url="/login")
def create(request):
    # When form is submitted
    if request.method == "POST":
        # Get form input
        title = request.POST["title"]
        start_bid = request.POST["bid"]
        image_url = request.POST["image"] if request.POST["image"] else " "
        description = request.POST["description"]
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
            # 1. Save it to the auction table
            auction.save()
            # 2. Update user record
            userId = request.user.id
            print(userId)
            current_user = User.objects.get(id=userId)
            # Empty auction list
            if current_user.auctions[0] == -1:
                current_user.auctions[0] = auction.id
            else:
                current_user.auctions = current_user.auctions + [auction.id]
            current_user.save()
            return HttpResponseRedirect(reverse("index"))
        # If missing value
        else:
            return render(request, "auctions/create.html", {
                "message" : "Please fill in all the blanks except image URL."
            })
    # Normal case
    return render(request, "auctions/create.html")


def listing(request, id, message=None, owner=None):
    # Two forms handling for POST method
    if request.method == "POST":
        # 1. Closing a bid by its owner
        if owner:
            return HttpResponseRedirect(reverse("listing", args=(id, )))
        # 2. Placing a new bid
        else:
            newBid = float(request.POST["newBid"])
            # 1. Find the highest bid so far
            bids = Bid.objects.all().filter(listing=id)
            if len(bids) > 0:
                highest_bid = max(bids, key=lambda bid: bid.new_bid)
            # 2. No bid has been placed so far, get the starting bid
            else:
                try:
                    listing = Auction.objects.get(id=id)
                    highest_bid = listing.start_bid
                except Auction.DoesNotExist:
                    print(f"Listing with id({id}) is not found.")
                    return render(request, "auctions/listing.html", {
                        "message": "Listing Not Found"
                    })
            # No bids so far, equal to start_bid is acceptable
            if newBid == highest_bid and len(bids) == 0:
                pass
            # A bid which is higher than the starting price can be placed
            elif newBid <= highest_bid:
                # "Bidding price must be at leaset as large as the starting bid"
                message = "Lower than start"
                return HttpResponseRedirect(reverse("listing_message", args=(id, message, )))
            # Place the bid
            Bid.objects.create(user=request.user.id, listing=id, new_bid=newBid)
            # "You have successfully placed a bid"
            message = "Success"
            return HttpResponseRedirect(reverse("listing_message", args=(id, message, )))


    # GET method
    try:
        listing = Auction.objects.get(id=id)
        print(listing)
        # Show different content to logged in user and non-logged in user
        loginStatus = True if request.user.is_authenticated else False
        
        # 1. For all users (#bids, highest_bid, owner)
        bids = Bid.objects.all().filter(listing=id)
        number_bids = len(bids)
        owner = User.objects.get(id=listing.createdBy)
        if number_bids > 0:
            highest_bid = max(bids, key=lambda bid: bid.new_bid)
            current_bid_price = highest_bid.new_bid
            # Current user has the highest bid currently or not
            if highest_bid.user == request.user.id:
                bid_message = "Your bid is the current bid."
        # No bids been placed so far
        else:
            current_bid_price = listing.start_bid
            bid_message = "No bid been placed yet"

        # 2. For login users (bid_message, watchlist)
        # Current user have added it to watchlist or not
        user = User.objects.get(id=request.user.id)
        inWatchlist = True if id in user.watchList else False

        # 3. For login uses + owner of the listing (close bid)
        ownerLogin = user if id in user.auctions else None
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "login": loginStatus,
            "message": message,
            "number_bids": number_bids,
            "current_bid": current_bid_price,
            "bid_message": bid_message,
            "inWatchlist": inWatchlist,
            "ownerLogin": ownerLogin,
            "owner": owner
        })
    except Auction.DoesNotExist:
        print(f"Listing with id({id}) is not found.")
        return render(request, "auctions/listing.html", {
            "message": "Listing Not Found"
        })





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



