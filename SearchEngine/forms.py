from django import forms
from .models import Search


class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('search',)


class SelectServer(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('select', 'search in all')