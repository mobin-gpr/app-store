from django import forms
from django.core import validators


class AppRequestForm(forms.Form):
    app_link = forms.CharField(
        widget=forms.URLInput(attrs={"class": "form-control", "id": "f-url"}),
        validators=[
            validators.RegexValidator(
                regex=r"^(https:\/\/play\.google\.com\/)",
                message="لینک وارد شده معتبر نیست.",
            )
        ],
    )
