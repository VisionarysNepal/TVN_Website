from django import forms

from apps.blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {"user_name", "email", "content"}

        widgets = {
            "user_name": forms.TextInput(
                attrs={"placeholder": "Your Name*", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Your Email*", "class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={"placeholder": "Your comment*", "class": "form-control"}
            ),
        }
