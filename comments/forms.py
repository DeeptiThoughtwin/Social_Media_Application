from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control break-words text-wrap', 
                'rows': 3, 
                'placeholder': 'Comment here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['body'].label = "" 
            
    