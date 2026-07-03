from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Story
from .forms import StoryForm


@login_required
def add_story(request):
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
    stories = Story.objects.all().order_by("-created_at")
    return render(request,"stories_list.html",{"stories": stories})


@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story,id=story_id,user=request.user)
    story.delete()
    return redirect("home")