from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-pink-500', 
                'rows': 3, 
                'placeholder': 'Comment here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = "" 
            
    