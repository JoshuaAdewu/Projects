from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import TagForm
from .models import Tag  # Test Tag model

# TODO: Remove temp prompt page
# Create tag submission form view
def prompt(request):
    # Display all tags and prompt for new tag
    response = "Please enter a new tag name."
    tags = Tag.objects.filter()
    context = {
        'tags': tags,
        'form': TagForm,
        'input_response': response
    }
    return render(request, "managetags/addtag.html", context=context)

# Create tag submission form view
def create(request):
    response = "Please enter a new tag name."  # Default response is invalid tag since no tag is added
    # Check for POST request for tag
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            # Create new Tag instance with given name
            newtag = Tag(name_text=str(form["tag_name"].value()))
            # Give success response if added, otherwise specify error.
            if newtag.add_new_tag():
                response = "Tag Successfully Added! Please enter a new tag name."
            elif not newtag.is_valid_name():
                response = "Invalid Tag Name. Please enter a new tag name."
            elif not newtag.is_new_tag():
                response = "Tag already exists. Please enter a new tag name."
    # Display all tags and re-prompt for next tag
    tags = Tag.objects.filter()
    context = {
        'tags': tags,
        'form': TagForm,
        'input_response': response
    }
    return render(request, "managetags/addtag.html", context=context)
