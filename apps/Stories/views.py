import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.Stories.models import Story
from apps.Stories.forms import StoryForm


logger = logging.getLogger(__name__)


class AddStoryView(LoginRequiredMixin, View):

    def get(self, request):
        logger.info(
            "Add story page viewed: user_id=%s",
            request.user.id
        )

        form = StoryForm()

        return render(
            request,
            "add_stories.html",
            {"form": form}
        )

    def post(self, request):
        form = StoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()

            logger.info(
                "Story created: story_id=%s user_id=%s",
                story.id,
                request.user.id
            )

            return redirect("home")

        logger.warning(
            "Story creation failed validation: user_id=%s",
            request.user.id
        )

        return render(
            request,
            "add_stories.html",
            {"form": form}
        )


class StoryListView(LoginRequiredMixin, View):

    def get(self, request):
        stories = Story.objects.all().order_by("-created_at")

        logger.info(
            "Story list viewed: user_id=%s story_count=%s",
            request.user.id,
            stories.count()
        )

        return render(
            request,
            "stories_list.html",
            {"stories": stories}
        )


class DeleteStoryView(LoginRequiredMixin, View):

    def post(self, request, story_id):
        story = get_object_or_404(
            Story,
            id=story_id,
            user=request.user
        )

        logger.info(
            "Story deleted: story_id=%s user_id=%s",
            story.id,
            request.user.id
        )

        story.delete()

        return redirect("home")