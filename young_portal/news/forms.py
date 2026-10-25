from django import forms
from .models import NewsComment
from .models import NewsPost


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Напишите ваш комментарий...',
                'class': 'form-control'
            }),
        }


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'content', 'portal_scope', 'image']  # подставь свои поля
