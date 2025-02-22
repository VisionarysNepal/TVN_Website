from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Subscribe


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = "__all__"

        labels = {"email": _("")}

        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your Email"}
            )
        }
