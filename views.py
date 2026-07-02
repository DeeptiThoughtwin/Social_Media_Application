from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Story
from .forms import StoryForm


@login_required
def add_story(request):
    """
    Upload a new story.
    """

    if request.method == "POST":

        form = StoryForm(request.POST, request.FILES)

        if form.is_valid():

            story = form.save(commit=False)

            story.user = request.user

            story.save()

            return redirect("feed")

    else:

        form = StoryForm()

    return render(
        request,
        "stories/add_story.html",
        {
            "form": form
        }
    )


@login_required
def story_list(request):
    """
    Display all active stories (last 24 hours).
    """

    stories = Story.objects.filter(
        expires_at__gt=timezone.now()
    ).order_by("-created_at")

    return render(
        request,
        "stories/story_list.html",
        {
            "stories": stories
        }
    )

@login_required
def delete_story(request, story_id):

    story = get_object_or_404(
        Story,
        id=story_id,
        user=request.user
    )

    story.delete()

    return redirect("feed")