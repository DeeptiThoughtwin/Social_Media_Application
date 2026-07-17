from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Story
from .forms import StoryForm


@login_required
def add_story(request):
    """Create and publish a new user story with optional media assets.

    Processes form text and file uploads on POST requests, attaches the newly
    created story instance to the currently authenticated user, and saves it
    to the database before routing the user back to the feed.

    Args:
        request (HttpRequest): The incoming HTTP request containing text form
            fields and multipart file streams.

    Returns:
        HttpResponseRedirect: Redirects to the 'home' view after a successful
            story creation.
        HttpResponse: Renders the 'add_stories.html' template populated with
            an empty or invalid StoryForm instance.
    """
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect("home")
    else:
        form = StoryForm()
    return render(request,"add_stories.html",{"form": form})


@login_required
def story_list(request):
    """Retrieve and display a chronological history of all stories.

    Queries every story record in the database, ordering them from the newest
    to the oldest creation timestamp, and forwards the collection to the
    listing view template.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders the 'stories_list.html' template populated with
            the global query set of stories.
    """
    stories = Story.objects.all().order_by("-created_at")
    return render(request,"stories_list.html",{"stories": stories})


@login_required
def delete_story(request, story_id):
    """Remove a specific story owned by the authenticated user.

    Fetches the targeted story by its primary key strictly validating that
    the requesting user matches the story's author record On confirmation
    the story instance is permanently deleted from the database.

    Args:
        request (HttpRequest): The incoming HTTP request.
        story_id (int): The primary key identifier of the story to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the 'home' view.
    """
    story = get_object_or_404(Story,id=story_id,user=request.user)
    story.delete()
    return redirect("home")
