from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Convert Markdown String to HTML format
    entry = util.get_entry(title)
    print(f"Current entry is: {title}") # Log message
    # Normal WIKI Page
    if entry:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "entry": entry
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
            # return HttpResponseRedirect(reverse("entry", result[0]))
            return HttpResponseRedirect(f"{result[0]}")
        # More than one match / no match at all
        else:
            return render(request, "encyclopedia/searchResults.html", {
                "matches": result
            })