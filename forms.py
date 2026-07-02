from django import forms
from .models import Story


class StoryForm(forms.ModelForm):

    class Meta:

        model = Story

        fields = ["image"]

        widgets = {

            "image": forms.FileInput(
                attrs={
                    "class": "hidden",
                    "accept": "image/*"
                }
            )

        }