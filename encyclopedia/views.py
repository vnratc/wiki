from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
#     # Use widget=forms.TextInput(attrs={}) to give atributes to the <form> html element
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia', 'class':'search'}))
    

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm
    })


def display_contents(request, title):
    if util.get_entry(title.lower()):   # if util.get_entry(title) != None:
        for t in util.list_entries():
            if t.lower() == title.lower(): title = t
        contents = util.get_entry(title)
        return render(request, "encyclopedia/contents.html", {
            "contents": contents,
            "form": SearchForm,
            "title": title
        })
    else:
        return render(request, 'encyclopedia/not_found.html', {
            "form": SearchForm,
        })

def search(request):
    if request.method == "POST":
        # Take in data from the submitted form
        form = SearchForm(request.POST)
        if form.is_valid():
            # Isolate value of form input named "q" from the 'cleaned' version of form data
            q = form.cleaned_data["q"]
            entries_l = [j.lower() for j in util.list_entries()]
            if q.lower() in entries_l:
                return display_contents(request, q)
            else:
                matches = [k for k in entries_l if q.lower() in k]
                return render(request, "encyclopedia/search_results.html", {
                    "matches": matches,
                    "form": SearchForm
                })
    else:
        return display_contents(request, "search")

class NewPage(forms.Form):
    page_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Title'}))
    page_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'aria-label': 'Markdown Content'}))

def new_page(request):
    if request.method == "POST":
        # Convert list to lowercase to compare with input
        entries_l = [j.lower() for j in util.list_entries()]
        new_page_form = NewPage(request.POST)
        if new_page_form.is_valid():
            new_page_title = new_page_form.cleaned_data["page_title"]
            new_page_content = new_page_form.cleaned_data["page_content"]
            if new_page_title.lower() in entries_l:
                return render(request, "encyclopedia/error_title.html", {
                    "new_page_title": new_page_title
                })
            else:
                util.save_entry(new_page_title, new_page_content)
                return display_contents(request, new_page_title)
    else:
        return render(request, "encyclopedia/new_page.html", {
            "new_page_form": NewPage
        })

def edit_page(request):
    if request.method == "POST":
        title_e = request.POST.get('title_e')
        #  Make sure title form the form is in entries
        for t in util.list_entries():
            if t.lower() == title_e.lower(): title_e = t
        contents_e = util.get_entry(title_e)
        # Create a form for editing and populate it
        class Edit(forms.Form):
            edit_title = forms.CharField(initial=title_e, widget=forms.HiddenInput())
            edit_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'aria-label': 'Markdown Content'}), initial=contents_e)

        return render(request, "encyclopedia/edit_page.html", {
            "form_e": Edit,
            "title_e": title_e
        })
    else:
        return display_contents(request, "edit_page")

def save_edit(request):
    if request.method == "POST":
        title_s = request.POST.get('edit_title')
        content_s = request.POST.get('edit_content')
        util.save_entry(title_s, content_s)
        return display_contents(request, title_s)
    else:
        return display_contents(request, "save_edit")