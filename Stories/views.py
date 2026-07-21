from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Story
from .forms import StoryForm


class AddStoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = StoryForm()
        return render(request, "add_stories.html", {"form": form})

    def post(self, request):
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect("home")
        return render(request, "add_stories.html", {"form": form})


class StoryListView(LoginRequiredMixin, View):
    def get(self, request):
        stories = Story.objects.all().order_by("-created_at")
        return render(request, "stories_list.html", {"stories": stories})


class DeleteStoryView(LoginRequiredMixin, View):
    def post(self, request, story_id):
        story = get_object_or_404(Story,id=story_id,user=request.user)
        story.delete()
        return redirect("home")

    