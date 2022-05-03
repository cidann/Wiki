from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    if util.get_entry(entry)==None:
        return HttpResponse("Entry not found")
    return render(request, "encyclopedia/entries.html",{"entry":entry,"content":util.get_entry(entry)})

