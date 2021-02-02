from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    # Convert Markdown String to HTML format
    entry = util.get_entry(title)
    print(entry)

    # Normal WIKI Page
    if entry:
        return render(request, "encyclopedia/entry.html",{
            "entry": entry
        })
    # Special Not Found Page
    else:
        return render(request, "encyclopedia/none.html")


