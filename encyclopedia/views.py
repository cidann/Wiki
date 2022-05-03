from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util

class SearchForm(forms.Form):
    search=forms.CharField(label="")

def index(request):
    if request.method=="POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            search=form.cleaned_data["search"]
            return HttpResponseRedirect(search)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form":SearchForm()
    })

def entries(request, entry):
    if entry not in util.list_entries():
        return HttpResponse("Entry not found")
    return render(request, "encyclopedia/entries.html",{"entry":entry,"content":util.get_entry(entry),"form":SearchForm()})

