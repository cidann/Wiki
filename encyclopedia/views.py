from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.urls import reverse
from random import random
from . import util



def index(request):
    if request.method=="POST":
        search=request.POST["q"]
        return HttpResponseRedirect(reverse("entries",args=[search]))
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    for i in util.list_entries():
        if entry.casefold()==i.casefold():
            entry=i
            content=util.convert(util.get_entry(entry))
            return render(request, "encyclopedia/entries.html", {"entry": entry, "content": content})
    search=[]
    for i in util.list_entries():
        if entry.casefold() in i.casefold():
            search.append(i)
    return render(request, "encyclopedia/searchresult.html",{"entry":entry,"search":search})


def create(request):
    if request.method=="POST":
        title=request.POST["title"]
        for i in util.list_entries():
            if title.casefold() == i.casefold():
                return HttpResponse("The Entry Already Exist")
        textarea=request.POST["textarea"]
        util.save_entry(title,textarea)
        return HttpResponseRedirect(reverse("entries",args=[title]))
    return render(request,"encyclopedia/create.html")

def edit(request,entry):
    if request.method=="POST":
        util.save_entry(entry,request.POST["textarea"])
        return HttpResponseRedirect(reverse("entries",args=[entry]))
    return render(request,"encyclopedia/edit.html",{"entry":entry,"content":util.get_entry(entry)})

def randomentry(request):
    randomEntryNumber = int(random()*len(util.list_entries()))
    entry=(util.list_entries())[randomEntryNumber]
    return HttpResponseRedirect(reverse("entries",args=[entry]))