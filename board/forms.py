from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "author", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input-field", "placeholder": "제목을 입력하세요"}),
            "author": forms.TextInput(attrs={"class": "input-field", "placeholder": "작성자명"}),
            "content": forms.Textarea(attrs={"class": "input-field", "rows": 8, "placeholder": "내용을 입력하세요"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "content"]
        widgets = {
            "author": forms.TextInput(attrs={"class": "input-field", "placeholder": "작성자명"}),
            "content": forms.Textarea(attrs={"class": "input-field", "rows": 3, "placeholder": "답글을 입력하세요"}),
        }
