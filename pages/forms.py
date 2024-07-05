from django import forms
from .models import Contact, Comment, Subscribe
from django.utils.text import gettext_lazy as _

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            "name" : forms.TextInput(attrs={
                "placeholder" : "Your Name",
                "class" : "form-control"
            }),
            "email" : forms.EmailInput(attrs={
                "placeholder" : "Your Email",
                "class" : "form-control"
            }),
            "subject" : forms.TextInput(attrs={
                "placeholder" : "Subject",
                "class" : "form-control"
            }),
            "message" : forms.Textarea(attrs={
                "placeholder" : "Message",
                "class" : "form-control",
                "rows" : 6
            })
        }

        labels = {
            "name" : "Your Name :",
            "email" : "Your Email :",
            "subject" : "Subject :",
            "message" : "Message :"
        }

        def clean(self):
            super(ContactForm, self).clean()

            name = self.cleaned_data.get("name")
            email = self.cleaned_data.get("email")
            subject = self.cleaned_data.get("subject")
            message = self.cleaned_data.get("message")


            if len(name) <= 0 or len(email) <= 0 or len(subject) <= 0 or len(message) <= 0:
                self.errors["name"] = self.error_class(["Shouldn't be empty."])

            return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {"user_name", "website",  "email", "content"}

        widgets = {
            "user_name" : forms.TextInput(attrs={
                "placeholder" : "Your Name*",
                "class" : "form-control"
            }),
            "email" : forms.EmailInput(attrs={
                "placeholder" : "Your Email*",
                "class" : "form-control"
            }),
            "website" : forms.TextInput(attrs={
                "placeholder" : "Your Website",
                "class" : "form-control"
            }),
            "content" : forms.Textarea(attrs={
                "placeholder" : "Your comment*",
                "class" : "form-control"
            }),
        }

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = "__all__"

        labels = {
            "email" : _("")
        }

        widgets = {
            "email" : forms.EmailInput(attrs={
                "class" : "form-control",
                "placeholder" : "Enter your Email"
            })
        }
