from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util

from random import choice
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Convert Markdown String to HTML format
    entry = util.get_entry(title)
    markdowner = Markdown()
    converted = markdowner.convert(entry)
    print(f"Current entry is: {title}") # Log message
    # Normal WIKI Page
    if entry:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "entry": converted
        })
    # Special Not Found Page
    else:
        return render(request, "encyclopedia/none.html")

def search(request):
    if request.method == "POST":
        # Get form input
        entry = request.POST["q"]
        # Always get the most up to date entries
        records = util.list_entries()
        result = []
        for record in records:
            if entry in record:
                result.append(record)
        print(f"Result options are: {result}")
        # Exact match
        if len(result) == 1:
            # @TODO: how to use reverse so no need to change the url everywhere
            # return HttpResponseRedirect(reverse("entry", args=(result[0]))
            return HttpResponseRedirect(reverse("entry", args=(result[0],)))
        # More than one match / no match at all
        else:
            return render(request, "encyclopedia/searchResults.html", {
                "matches": result
            })

def create(request):
    # When save button is clicked
    if request.method == "POST":
        # Get form input
        title = request.POST["title"]
        content = request.POST["content"]
        # Create helper function 
        createHelper(title, content)
        # Redirect to the entry page
        return HttpResponseRedirect(reverse("entry", args=(title,)))
    # Get method, go to the edit page
    return render(request, "encyclopedia/createEntry.html")

def random(request):
    # Always get the most up to date entries
    records = util.list_entries()
    return HttpResponseRedirect(reverse("entry", args=(choice(records),)))

def edit(request, title):
    # Submitting changes made to the entry
    if request.method == "POST":
        content = request.POST["content"]
        print(content)
        # Create helper function
        createHelper(title, content, True)
        # Redirect to the entry page
        return HttpResponseRedirect(reverse("entry", args=(title,)))
    entry = util.get_entry(title)
    # Default info page
    return render(request, "encyclopedia/editEntry.html",{
        "title": title,
        "entry": entry
    } )


def createHelper(title, content, update=False):
    print(update)
    if len(title) > 0 and len(content) > 0:
        # Check if the entry exist
        # Always get the most up to date entries
        records = util.list_entries()
        # Already exist
        if title in records:
            # @TODO: Error Message
            print(f"{title} already exists")

            # User should be able to update the content when accessing through edit page
            if update:
                util.save_entry(title, content)
        else:
            # Store new context into our database through util functions
            util.save_entry(title, content)