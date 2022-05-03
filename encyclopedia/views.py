from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util

class SearchForm(forms.Form):
    search=forms.CharField(label="")

def index(request):
    if request.method=="POST":
        search=request.POST["q"]
        return HttpResponseRedirect(search)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form":SearchForm()
    })

def entries(request, entry):
    if entry not in util.list_entries():
        search=[]
        for i in util.list_entries():
            if entry.casefold() in i.casefold():
                search.append(i)
        return render(request, "encyclopedia/searchresult.html",{"entry":entry,"search":search})
    return render(request, "encyclopedia/entries.html",{"entry":entry,"content":util.get_entry(entry)})

