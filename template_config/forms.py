from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "q-search-text",
                "name": "s",
                "placeholder": "دنبال چی هستید...",
            }
        )
    )
